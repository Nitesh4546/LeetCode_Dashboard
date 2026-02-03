import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QCursor
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt, QCoreApplication
import leetcode_backend as lb

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Backend Instances
    leetcode = lb.LeetCodeStats()
    heatmap = lb.HeatmapBackend()
    contests = lb.ContestBackend()

    root_context = engine.rootContext()
    root_context.setContextProperty("leetcode", leetcode)
    root_context.setContextProperty("heatmap", heatmap)
    root_context.setContextProperty("contestBackend", contests)

    qml_file = Path(__file__).parent / "main.qml"
    engine.load(str(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]

    # Feature: Always on Top and Frameless for the glossy look
    window.setFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    # Feature: Close when clicked outside
    def handle_focus_loss():
        if not window.property("active"):
            cursor_pos = QCursor.pos()
            window_geo = window.geometry()
            # If mouse is outside the window area when focus is lost (click outside)
            if not window_geo.contains(cursor_pos):
                QCoreApplication.quit()

    window.activeChanged.connect(handle_focus_loss)

    sys.exit(app.exec())
