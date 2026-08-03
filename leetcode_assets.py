import json
import os
import logging
from datetime import datetime, timezone, timedelta
from collections import OrderedDict
from typing import Optional, TypedDict, Any

import requests

import config

log = logging.getLogger(__name__)

DATA_DIR = "./data"
DATA_FILE = os.path.join(DATA_DIR, "info.json")


class StatsData(TypedDict, total=False):
    username: str
    ranking: str
    totalProblems: int
    totalSolved: int
    easySolved: int
    easyTotal: int
    mediumSolved: int
    mediumTotal: int
    hardSolved: int
    hardTotal: int
    contest: list
    submissionCalendar: dict


# ---------------------------------------------------------------------------
# Fetch / cache
# ---------------------------------------------------------------------------

def _is_cache_fresh() -> bool:
    if not os.path.exists(DATA_FILE):
        return False
    age = datetime.now().timestamp() - os.path.getmtime(DATA_FILE)
    return age < config.CACHE_TTL_MINUTES * 60


def fetch_remote(username: str) -> Optional[StatsData]:
    """Fetch fresh data from the API. Returns None on any failure (never raises)."""
    profile_url = f"{config.BASE_URL}/{username}/profile"
    contest_url = f"{config.BASE_URL}/contests/upcoming"

    try:
        r_profile = requests.get(profile_url, timeout=10)
        r_profile.raise_for_status()
        r_contest = requests.get(contest_url, timeout=10)
        r_contest.raise_for_status()
    except requests.RequestException as e:
        log.warning("LeetCode API request failed: %s", e)
        return None

    try:
        info = r_profile.json()
    except ValueError:
        log.warning("Profile response was not valid JSON")
        return None

    data: StatsData = {
        "username": username,
        "ranking": f"{int(info['ranking']):,}" if info.get("ranking") not in ("N/A", None) else "N/A",
        "totalProblems": info.get("totalQuestions", 0),
        "totalSolved": info.get("totalSolved", 0),
        "easySolved": info.get("easySolved", 0),
        "easyTotal": info.get("totalEasy", 1),
        "mediumSolved": info.get("mediumSolved", 0),
        "mediumTotal": info.get("totalMedium", 1),
        "hardSolved": info.get("hardSolved", 0),
        "hardTotal": info.get("totalHard", 1),
        "contest": r_contest.json().get("contests", []),
        "submissionCalendar": info.get("submissionCalendar", {}),
    }
    return data


def _save_cache(data: StatsData) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def _load_cache() -> Optional[StatsData]:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log.info("No usable local cache: %s", e)
        return None


def load_data(username: str = config.USERNAME, force_refresh: bool = False) -> Optional[StatsData]:
    """
    Returns stats data, preferring a fresh remote fetch, falling back to the
    local cache (any age) if the network call fails, and returning None only
    if neither is available. Never raises.
    """
    if not force_refresh and _is_cache_fresh():
        cached = _load_cache()
        if cached:
            return cached

    fresh = fetch_remote(username)
    if fresh:
        _save_cache(fresh)
        return fresh

    log.warning("Falling back to stale/local cache (remote fetch failed)")
    return _load_cache()


# ---------------------------------------------------------------------------
# Module state — populated explicitly via refresh(), NOT at import time
# ---------------------------------------------------------------------------

_info: Optional[StatsData] = None
_raw_submissions: dict = {}


def refresh(force: bool = False) -> bool:
    """Call this explicitly (e.g. from a background thread) to (re)load data."""
    global _info, _raw_submissions
    _info = load_data(force_refresh=force)
    _raw_submissions = (_info or {}).get("submissionCalendar", {}) or {}
    return _info is not None


# ---------------------------------------------------------------------------
# Accessors used by the Qt backend
# ---------------------------------------------------------------------------

def get_leetcode_stats() -> dict:
    if not _info:
        return {"username": config.USERNAME, "ranking": "N/A", "totalSolved": 0}
    return {
        "username": _info.get("username"),
        "ranking": _info.get("ranking", "N/A"),
        "totalProblems": _info.get("totalProblems", 0),
        "totalSolved": _info.get("totalSolved", 0),
        "easySolved": _info.get("easySolved", 0),
        "easyTotal": _info.get("easyTotal", 1),
        "mediumSolved": _info.get("mediumSolved", 0),
        "mediumTotal": _info.get("mediumTotal", 1),
        "hardSolved": _info.get("hardSolved", 0),
        "hardTotal": _info.get("hardTotal", 1),
    }


def get_contest_data() -> list:
    """Filters to return only the nearest Weekly and Biweekly contests."""
    if not _info or "contest" not in _info:
        return []

    nearest_weekly = None
    nearest_biweekly = None

    for c in _info["contest"]:
        title = c.get("title", "")
        if "Biweekly" in title and not nearest_biweekly:
            nearest_biweekly = c
        elif "Weekly" in title and not nearest_weekly:
            nearest_weekly = c
        if nearest_weekly and nearest_biweekly:
            break

    selected = [c for c in (nearest_weekly, nearest_biweekly) if c]
    selected.sort(key=lambda x: x["startTime"])

    formatted = []
    for c in selected:
        dt = datetime.fromtimestamp(c["startTime"], tz=timezone.utc)
        formatted.append({
            "title": c["title"],
            "slug": c["titleSlug"],
            "startTime": dt.strftime("%b %d, %Y %I:%M %p"),
            "duration": f"{c['duration'] // 60} mins",
            "isWeekly": "Weekly" in c["title"] and "Biweekly" not in c["title"],
        })
    return formatted


def get_color(count: int) -> str:
    if count == 0: return "#2d2d2d"
    if count <= 3: return "#0e4429"
    if count <= 7: return "#006d32"
    if count <= 12: return "#26a641"
    return "#39d353"


def get_heatmap_data() -> list:
    """Returns formatted submission calendar data for a 9-month window."""
    data = {int(k): v for k, v in _raw_submissions.items()}
    if not data:
        return []

    latest_ts = max(data.keys())
    end_dt = datetime.fromtimestamp(latest_ts, tz=timezone.utc).date()
    start_dt = end_dt - timedelta(days=274)

    months_dict: "OrderedDict[str, list]" = OrderedDict()
    curr = start_dt
    while curr <= end_dt:
        month_key = curr.strftime("%b")
        months_dict.setdefault(month_key, [])
        ts_lookup = int(datetime(curr.year, curr.month, curr.day, tzinfo=timezone.utc).timestamp())
        count = data.get(ts_lookup, 0)
        months_dict[month_key].append({
            "date": curr.strftime("%b %d, %Y"),
            "count": count,
            "color": get_color(count),
        })
        curr += timedelta(days=1)

    return [{"monthName": name, "days": days} for name, days in months_dict.items()]


def get_streak_data() -> tuple[int, int]:
    if not _raw_submissions:
        return 0, 0
    dates = sorted({datetime.fromtimestamp(int(ts), tz=timezone.utc).date() for ts in _raw_submissions.keys()})
    if not dates:
        return 0, 0

    max_streak = 0
    temp_streak = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            temp_streak += 1
        else:
            max_streak = max(max_streak, temp_streak)
            temp_streak = 1
    max_streak = max(max_streak, temp_streak)

    last_date = dates[-1]
    count = 0
    expected_date = last_date
    for d in reversed(dates):
        if d == expected_date:
            count += 1
            expected_date -= timedelta(days=1)
        else:
            break
    return max_streak, count