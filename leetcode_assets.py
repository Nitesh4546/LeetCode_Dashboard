import json
import os
from datetime import datetime, timezone, timedelta
from collections import OrderedDict
import requests

BASE_URL = "https://alfa-leetcode-api.onrender.com/"
USERNAME = "YOUR_NAME"

def create(username):
    # Ensure the data directory exists
    os.makedirs("./data", exist_ok=True)

    profile = f"{BASE_URL}/{username}/profile"
    contest = f"{BASE_URL}/contests/upcoming"

    try:
        response = requests.get(profile, timeout=10)
        response_con = requests.get(contest, timeout=10)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

    if response.status_code == 200 and response_con.status_code == 200:
        info = response.json()
        data = {
            "username": username,
            "ranking": f"{int(info['ranking']):,}" if info.get('ranking') not in ["N/A", None] else "N/A",
            "totalProblems": info.get("totalQuestions", 0),
            "totalSolved": info.get("totalSolved", 0),
            "easySolved": info.get("easySolved", 0),
            "easyTotal": info.get("totalEasy", 1),
            "mediumSolved": info.get("mediumSolved", 0),
            "mediumTotal": info.get("totalMedium", 1),
            "hardSolved": info.get("hardSolved", 0),
            "hardTotal": info.get("totalHard", 1),
            "contest": response_con.json().get("contests", []), # Save ALL contests
            "submissionCalendar": info.get("submissionCalendar")
        }
        with open("./data/info.json", "w") as file:
            file.write(json.dumps(data, indent=4))
        return True
    return False

# Initial data fetch
create(USERNAME)

def load_local_data():
    try:
        with open('./data/info.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

info = load_local_data()
RAW_SUBMISSIONS = info.get("submissionCalendar", {}) if info else {}

def get_leetcode_stats():
    if not info:
        return {"username": USERNAME, "ranking": "N/A", "totalSolved": 0}
    return {
        "username": info.get("username"),
        "ranking": info.get("ranking", "N/A"),
        "totalProblems": info.get("totalProblems", 0),
        "totalSolved": info.get("totalSolved", 0),
        "easySolved": info.get("easySolved", 0),
        "easyTotal": info.get("easyTotal", 1),
        "mediumSolved": info.get("mediumSolved", 0),
        "mediumTotal": info.get("mediumTotal", 1),
        "hardSolved": info.get("hardSolved", 0),
        "hardTotal": info.get("hardTotal", 1)
    }

def get_contest_data():
    """Filters to return only the nearest Weekly and Biweekly contests."""
    if not info or "contest" not in info:
        return []

    nearest_weekly = None
    nearest_biweekly = None

    # API usually returns contests sorted by startTime
    for c in info["contest"]:
        title = c.get("title", "")
        if "Biweekly" in title and not nearest_biweekly:
            nearest_biweekly = c
        elif "Weekly" in title and not nearest_weekly:
            nearest_weekly = c

        if nearest_weekly and nearest_biweekly:
            break

    # Combine found contests and format them
    selected = []
    if nearest_weekly: selected.append(nearest_weekly)
    if nearest_biweekly: selected.append(nearest_biweekly)

    # Ensure they are displayed in chronological order
    selected.sort(key=lambda x: x["startTime"])

    formatted_contests = []
    for c in selected:
        dt = datetime.fromtimestamp(c["startTime"])
        formatted_contests.append({
            "title": c["title"],
            "slug": c["titleSlug"],
            "startTime": dt.strftime("%b %d, %Y %I:%M %p"),
            "duration": f"{c['duration'] // 60} mins",
            "isWeekly": "Weekly" in c["title"] and "Biweekly" not in c["title"]
        })
    return formatted_contests

def get_color(count):
    if count == 0: return "#2d2d2d"
    if count <= 3: return "#0e4429"
    if count <= 7: return "#006d32"
    if count <= 12: return "#26a641"
    return "#39d353"

# def get_heatmap_data():
#     data = {int(k): v for k, v in RAW_SUBMISSIONS.items()}
#     if not data: return []
#     latest_ts = max(data.keys())
#     end_dt = datetime.fromtimestamp(latest_ts, tz=timezone.utc).date()
#     start_dt = (end_dt - timedelta(days=182))
#     months_dict = OrderedDict()
#     curr = start_dt
#     while curr <= end_dt:
#         month_key = curr.strftime("%b")
#         if month_key not in months_dict:
#             months_dict[month_key] = []
#         ts_lookup = int(datetime(curr.year, curr.month, curr.day, tzinfo=timezone.utc).timestamp())
#         count = data.get(ts_lookup, 0)
#         months_dict[month_key].append({
#             "date": curr.strftime("%b %d, %Y"),
#             "count": count,
#             "color": get_color(count)
#         })
#         curr += timedelta(days=1)
#     return [{"monthName": name, "days": days} for name, days in months_dict.items()]

def get_heatmap_data():
    """Returns formatted submission calendar data for a 9-month window."""
    data = {int(k): v for k, v in RAW_SUBMISSIONS.items()}
    if not data: return []

    latest_ts = max(data.keys())
    end_dt = datetime.fromtimestamp(latest_ts, tz=timezone.utc).date()

    # Updated: Set to 274 days for a 9-month history
    start_dt = (end_dt - timedelta(days=274))

    months_dict = OrderedDict()
    curr = start_dt

    while curr <= end_dt:
        month_key = curr.strftime("%b")
        if month_key not in months_dict:
            months_dict[month_key] = []

        ts_lookup = int(datetime(curr.year, curr.month, curr.day, tzinfo=timezone.utc).timestamp())
        count = data.get(ts_lookup, 0)

        months_dict[month_key].append({
            "date": curr.strftime("%b %d, %Y"),
            "count": count,
            "color": get_color(count)
        })
        curr += timedelta(days=1)

    return [{"monthName": name, "days": days} for name, days in months_dict.items()]

def get_streak_data():
    if not RAW_SUBMISSIONS: return 0, 0
    dates = sorted({datetime.fromtimestamp(int(ts), tz=timezone.utc).date() for ts in RAW_SUBMISSIONS.keys()})
    if not dates: return 0, 0
    max_streak = 0
    temp_streak = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i-1] + timedelta(days=1):
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
        else: break
    return max_streak, count
