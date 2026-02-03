# LeetCode Dashboard

A high-performance, dark-themed dashboard designed for the Linux desktop (optimized for Hyprland/Quickshell). This application provides a real-time overview of your LeetCode progress, activity heatmap, and upcoming contests in a glossy, frameless overlay.

## 🚀 Features

* **Dynamic Progress Visualization**: Three concentric rings visualizing Easy, Medium, and Hard problems solved with interactive hover states.
* **9-Month Contribution Heatmap**: A GitHub-style activity tracker calculating streaks and submission intensity.
* **Contest Tracker**: Displays the nearest Weekly and Biweekly contests with animated backgrounds and direct links.
* **Glossy Linux UI**: Frameless, "always-on-top" design that automatically closes when focus is lost—perfect for a modern desktop rice.

---

## 🛠️ Tech Stack

* **Frontend**: QML (Qt Quick) with `Qt5Compat` for graphical effects.
* **Backend**: Python 3.x using PySide6 for data processing and Qt signal management.
* **Data Source**: LeetCode API (via `alfa-leetcode-api`).

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | Entry point. Handles window flags, focus management, and bridges Python to QML. |
| `main.qml` | The primary UI layout using `Flickable`, `ColumnLayout`, and `Shapes`. |
| `leetcode_backend.py` | Defines `QObject` classes that expose data to QML via `Property` and `Signal`. |
| `leetcode_assets.py` | Handles API requests, JSON caching, and streak/heatmap algorithms. |
| `/data/info.json` | Local cache to store profile and contest data for faster loading. |

---

## ⚙️ Installation & Usage

### 1. Prerequisites
Ensure you have Python installed with the necessary libraries:
```bash
pip install PySide6 requests
