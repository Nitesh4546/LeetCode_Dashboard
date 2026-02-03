from PySide6.QtCore import QObject, Property, Signal, QTimer
# from leetcode_assets import get_leetcode_stats
import leetcode_assets as la

class LeetCodeStats(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        # Initialize with empty/default data first
        self._stats = {}
        # Use a single-shot timer to load data after the UI is ready
        QTimer.singleShot(100, self.load_data)

    def load_data(self):
        self._stats = la.get_leetcode_stats()
        self.dataChanged.emit() # This signal triggers the QML sweep

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
        # Initialize data from assets
        self._heatmap_data = la.get_heatmap_data()
        self._current_streak, self._max_streak = la.get_streak_data()

    @Property("QVariantList", notify=dataChanged)
    def heatmapData(self): return self._heatmap_data

    @Property(int, notify=dataChanged)
    def totalSubmissions(self):
        return sum(d['count'] for m in self._heatmap_data for d in m['days'])

    @Property(int, notify=dataChanged)
    def currentStreak(self): return self._current_streak

    @Property(int, notify=dataChanged)
    def maxStreak(self): return self._max_streak

class ContestBackend(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._contests = la.get_contest_data()

    @Property("QVariantList", notify=dataChanged)
    def contestModel(self):
        return self._contests
