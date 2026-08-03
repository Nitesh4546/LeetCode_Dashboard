import logging
from PySide6.QtCore import QObject, Property, Signal, QThread

import leetcode_assets as la

log = logging.getLogger(__name__)


class _RefreshWorker(QThread):
    """Runs the network fetch off the UI thread."""
    finished_ok = Signal(bool)

    def __init__(self, force: bool = False, parent=None):
        super().__init__(parent)
        self._force = force

    def run(self):
        ok = la.refresh(force=self._force)
        self.finished_ok.emit(ok)


class LeetCodeStats(QObject):
    dataChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()

    def __init__(self):
        super().__init__()
        self._stats = {}
        self._loading = True
        self._error = ""
        self._worker = None
        self.refresh()

    def refresh(self, force: bool = False):
        self._loading = True
        self.loadingChanged.emit()
        self._worker = _RefreshWorker(force=force)
        self._worker.finished_ok.connect(self._on_loaded)
        self._worker.start()

    def _on_loaded(self, ok: bool):
        self._stats = la.get_leetcode_stats()
        self._error = "" if ok else "Unable to fetch LeetCode data — showing cached/last-known values."
        self._loading = False
        self.loadingChanged.emit()
        self.errorChanged.emit()
        self.dataChanged.emit()

    @Property(bool, notify=loadingChanged)
    def loading(self): return self._loading

    @Property(str, notify=errorChanged)
    def errorMessage(self): return self._error

    @Property(int, notify=dataChanged)
    def totalSolved(self): return self._stats.get("totalSolved", 0)

    @Property(int, notify=dataChanged)
    def totalProblems(self): return self._stats.get("totalProblems", 1)

    @Property(int, notify=dataChanged)
    def easySolved(self): return self._stats.get("easySolved", 0)

    @Property(int, notify=dataChanged)
    def easyTotal(self): return self._stats.get("easyTotal", 1)

    @Property(int, notify=dataChanged)
    def mediumSolved(self): return self._stats.get("mediumSolved", 0)

    @Property(int, notify=dataChanged)
    def mediumTotal(self): return self._stats.get("mediumTotal", 1)

    @Property(int, notify=dataChanged)
    def hardSolved(self): return self._stats.get("hardSolved", 0)

    @Property(int, notify=dataChanged)
    def hardTotal(self): return self._stats.get("hardTotal", 1)

    @Property(str, notify=dataChanged)
    def ranking(self): return str(self._stats.get("ranking", "N/A"))


class HeatmapBackend(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._heatmap_data = []
        self._current_streak = 0
        self._max_streak = 0

    def refreshFromCache(self):
        """Call after LeetCodeStats has finished loading so data is available."""
        self._heatmap_data = la.get_heatmap_data()
        self._current_streak, self._max_streak = la.get_streak_data()
        self.dataChanged.emit()

    @Property("QVariantList", notify=dataChanged)
    def heatmapData(self): return self._heatmap_data

    @Property(int, notify=dataChanged)
    def totalSubmissions(self):
        return sum(d["count"] for m in self._heatmap_data for d in m["days"])

    @Property(int, notify=dataChanged)
    def currentStreak(self): return self._current_streak

    @Property(int, notify=dataChanged)
    def maxStreak(self): return self._max_streak


class ContestBackend(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._contests = []

    def refreshFromCache(self):
        self._contests = la.get_contest_data()
        self.dataChanged.emit()

    @Property("QVariantList", notify=dataChanged)
    def contestModel(self):
        return self._contests