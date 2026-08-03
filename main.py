import sys
import logging
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QCursor
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt, QCoreApplication

import config  # noqa: F401  (validates .env / raises early if misconfigured)
import leetcode_backend as lb

log = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Backend instances
    leetcode = lb.LeetCodeStats()
    heatmap = lb.HeatmapBackend()
    contests = lb.ContestBackend()

    # Heatmap/contest data depends on the same fetch LeetCodeStats triggers,
    # so populate them once that fetch completes instead of guessing a delay.
    leetcode.dataChanged.connect(heatmap.refreshFromCache)
    leetcode.dataChanged.connect(contests.refreshFromCache)

    root_context = engine.rootContext()
    root_context.setContextProperty("leetcode", leetcode)
    root_context.setContextProperty("heatmap", heatmap)
    root_context.setContextProperty("contestBackend", contests)

    qml_file = Path(__file__).parent / "main.qml"
    engine.load(str(qml_file))

    if not engine.rootObjects():
        log.error("Failed to load QML file: %s", qml_file)
        sys.exit(-1)

    window = engine.rootObjects()[0]

    # Feature: Always on Top and Frameless for the glossy look
    window.setFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    # Feature: Close when clicked outside the window
    def handle_focus_loss():
        if not window.property("active"):
            cursor_pos = QCursor.pos()
            window_geo = window.geometry()
            if not window_geo.contains(cursor_pos):
                QCoreApplication.quit()

    window.activeChanged.connect(handle_focus_loss)

    sys.exit(app.exec())