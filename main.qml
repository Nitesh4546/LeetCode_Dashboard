import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Shapes 1.15
import Qt5Compat.GraphicalEffects 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 1120
    height: 950
    minimumWidth: 1120
    maximumWidth: 1120
    minimumHeight: 950
    maximumHeight: 950

    title: "LeetCode Dashboard"
    color: "#0a0a0a"

    // Closes the application when clicking the background
    MouseArea {
        anchors.fill: parent
        z: -1
        onPressed: Qt.quit()
    }

    Flickable {
        anchors.fill: parent
        contentHeight: mainLayout.height + 100
        clip: true
        ScrollBar.vertical: ScrollBar { }

        ColumnLayout {
            id: mainLayout
            width: parent.width - 60
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 30
            spacing: 50

            // =========================================================
            // SECTION 1: LEETCODE DASHBOARD
            // =========================================================
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 25

                RowLayout {
                    Layout.fillWidth: true
                    Column {
                        spacing: 4
                        Row {
                            spacing: 8
                            Image {
                                id: leetcodeLogo
                                source: "./img/leetcode.png"
                                sourceSize.width: 32; sourceSize.height: 32
                            }
                            Text {
                                text: "LeetCode"; color: "#ffa116"; font.pixelSize: 22; font.bold: true
                                anchors.verticalCenter: leetcodeLogo.verticalCenter
                            }
                        }
                        Text { text: "Nitesh_Nunia"; color: "white"; font.pixelSize: 18; leftPadding: 5 }
                    }
                    Item { Layout.fillWidth: true }
                    Column {
                        Layout.alignment: Qt.AlignRight | Qt.AlignTop
                        Text { text: "Rank"; color: "#888"; font.pixelSize: 12; horizontalAlignment: Text.AlignRight; width: parent.width }
                        Text {
                            text: leetcode ? leetcode.ranking : "N/A"
                            color: "white"; font.pixelSize: 22; font.bold: true; horizontalAlignment: Text.AlignRight
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 50

                    Item {
                        id: progressShape
                        width: 260; height: 260
                        property string hoveredDifficulty: ""

                        readonly property real easySweep: leetcode ? (leetcode.easySolved / Math.max(1, leetcode.easyTotal)) * 360 : 0
                        readonly property real medSweep: leetcode ? (leetcode.mediumSolved / Math.max(1, leetcode.mediumTotal)) * 360 : 0
                        readonly property real hardSweep: leetcode ? (leetcode.hardSolved / Math.max(1, leetcode.hardTotal)) * 360 : 0

                        Shape {
                            anchors.fill: parent; layer.enabled: true; layer.samples: 4
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#1a2d2a"; strokeWidth: 12
                                PathAngleArc { centerX: 130; centerY: 130; radiusX: 110; radiusY: 110; startAngle: 0; sweepAngle: 360 }
                            }
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#00b8a3"; strokeWidth: 12; capStyle: ShapePath.RoundCap
                                PathAngleArc {
                                    centerX: 130; centerY: 130; radiusX: 110; radiusY: 110; startAngle: -90
                                    sweepAngle: progressShape.easySweep
                                    Behavior on sweepAngle { NumberAnimation { duration: 1200; easing.type: Easing.OutQuart } }
                                }
                            }
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#2d2a1a"; strokeWidth: 12
                                PathAngleArc { centerX: 130; centerY: 130; radiusX: 92; radiusY: 92; startAngle: 0; sweepAngle: 360 }
                            }
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#ffc01e"; strokeWidth: 12; capStyle: ShapePath.RoundCap
                                PathAngleArc {
                                    centerX: 130; centerY: 130; radiusX: 92; radiusY: 92; startAngle: -90
                                    sweepAngle: progressShape.medSweep
                                    Behavior on sweepAngle { NumberAnimation { duration: 1500; easing.type: Easing.OutQuart } }
                                }
                            }
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#2d1a1e"; strokeWidth: 12
                                PathAngleArc { centerX: 130; centerY: 130; radiusX: 74; radiusY: 74; startAngle: 0; sweepAngle: 360 }
                            }
                            ShapePath {
                                fillColor: "transparent"; strokeColor: "#ff375f"; strokeWidth: 12; capStyle: ShapePath.RoundCap
                                PathAngleArc {
                                    centerX: 130; centerY: 130; radiusX: 74; radiusY: 74; startAngle: -90
                                    sweepAngle: progressShape.hardSweep
                                    Behavior on sweepAngle { NumberAnimation { duration: 1800; easing.type: Easing.OutQuart } }
                                }
                            }
                        }

                        Column {
                            anchors.centerIn: parent
                            spacing: -2
                            Text {
                                text: {
                                    if (progressShape.hoveredDifficulty === "Easy") return leetcode.easySolved + " / " + leetcode.easyTotal
                                        if (progressShape.hoveredDifficulty === "Medium") return leetcode.mediumSolved + " / " + leetcode.mediumTotal
                                            if (progressShape.hoveredDifficulty === "Hard") return leetcode.hardSolved + " / " + leetcode.hardTotal
                                                return (leetcode ? leetcode.totalSolved : "0") + " / " + (leetcode ? leetcode.totalProblems : "0")
                                }
                                color: "white"; font.pixelSize: 18; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter
                            }
                            Text {
                                text: progressShape.hoveredDifficulty !== "" ? progressShape.hoveredDifficulty : "Solved"
                                color: "#888"; font.pixelSize: 14; anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }

                        MouseArea {
                            anchors.fill: parent; hoverEnabled: true
                            onPositionChanged: {
                                var dist = Math.sqrt(Math.pow(mouseX - 130, 2) + Math.pow(mouseY - 130, 2))
                                if (dist >= 104 && dist <= 116) progressShape.hoveredDifficulty = "Easy"
                                    else if (dist >= 86 && dist <= 98) progressShape.hoveredDifficulty = "Medium"
                                        else if (dist >= 68 && dist <= 80) progressShape.hoveredDifficulty = "Hard"
                                            else progressShape.hoveredDifficulty = ""
                            }
                            onExited: progressShape.hoveredDifficulty = ""
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true; spacing: 25
                        Repeater {
                            model: leetcode ? [
                                { label: "Easy", solved: leetcode.easySolved, total: leetcode.easyTotal, color: "#00b8a3" },
                                { label: "Medium", solved: leetcode.mediumSolved, total: leetcode.mediumTotal, color: "#ffc01e" },
                                { label: "Hard", solved: leetcode.hardSolved, total: leetcode.hardTotal, color: "#ff375f" }
                            ] : []
                            delegate: ColumnLayout {
                                Layout.fillWidth: true; spacing: 8
                                RowLayout {
                                    Text { text: modelData.label; color: "#aaa"; font.pixelSize: 16 }
                                    Item { Layout.fillWidth: true }
                                    Text { text: modelData.solved + " / " + modelData.total; color: "white"; font.pixelSize: 16; font.bold: true }
                                }
                                Rectangle {
                                    Layout.fillWidth: true; height: 8; color: "#2d2d2d"; radius: 4
                                    Rectangle {
                                        width: parent.width * (modelData.solved / Math.max(1, modelData.total))
                                        height: 8; color: modelData.color; radius: 4
                                        Behavior on width { NumberAnimation { duration: 1000; easing.type: Easing.OutCubic } }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // =========================================================
            // SECTION 2: CONTRIBUTION HEATMAP (12 MONTHS)
            // =========================================================
            ColumnLayout {
                Layout.fillWidth: true; spacing: 15
                RowLayout {
                    Layout.fillWidth: true
                    Column {
                        spacing: 4
                        Text { text: (heatmap ? heatmap.totalSubmissions : 0) + " submissions"; color: "white"; font.pixelSize: 22; font.bold: true }
                        Row {
                            spacing: 15
                            Text { text: "Current Streak: " + (heatmap ? heatmap.currentStreak : 0) + " days"; color: "#39d353"; font.pixelSize: 13 }
                            Text { text: "Max Streak: " + (heatmap ? heatmap.maxStreak : 0) + " days"; color: "#aaaaaa"; font.pixelSize: 13 }
                        }
                    }
                    Item { Layout.fillWidth: true }
                    Row {
                        spacing: 4
                        Text { text: "Less "; color: "#888"; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                        Rectangle { width: 12; height: 12; color: "#2d2d2d"; radius: 2 }
                        Rectangle { width: 12; height: 12; color: "#0e4429"; radius: 2 }
                        Rectangle { width: 12; height: 12; color: "#006d32"; radius: 2 }
                        Rectangle { width: 12; height: 12; color: "#26a641"; radius: 2 }
                        Rectangle { width: 12; height: 12; color: "#39d353"; radius: 2 }
                        Text { text: " More"; color: "#888"; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                    }
                }

                RowLayout {
                    spacing: 10; Layout.fillWidth: true
                    Column {
                        spacing: 0
                        Item { width: 30; height: 26 }
                        Item { width: 30; height: 18 }
                        Text { text: "Mon"; color: "#888"; font.pixelSize: 11; height: 14; width: 30; verticalAlignment: Text.AlignVCenter }
                        Item { width: 30; height: 22 }
                        Text { text: "Wed"; color: "#888"; font.pixelSize: 11; height: 14; width: 30; verticalAlignment: Text.AlignVCenter }
                        Item { width: 30; height: 22 }
                        Text { text: "Fri"; color: "#888"; font.pixelSize: 11; height: 14; width: 30; verticalAlignment: Text.AlignVCenter }
                    }

                    Flickable {
                        Layout.fillWidth: true
                        height: 170
                        contentWidth: heatmapRow.width
                        clip: true
                        boundsBehavior: Flickable.StopAtBounds
                        ScrollBar.horizontal: ScrollBar { policy: ScrollBar.AsNeeded; active: true }

                        Row {
                            id: heatmapRow
                            spacing: 18
                            Repeater {
                                model: heatmap ? heatmap.heatmapData : []
                                delegate: Column {
                                    spacing: 10
                                    Text { text: modelData.monthName; color: "#b3b3b3"; font.pixelSize: 14; font.bold: true }
                                    Grid {
                                        rows: 7; flow: Grid.TopToBottom; spacing: 4
                                        Repeater {
                                            model: modelData.days
                                            delegate: Rectangle {
                                                id: dayRect
                                                width: 14; height: 14; radius: 2; color: modelData.color
                                                MouseArea {
                                                    anchors.fill: parent; hoverEnabled: true
                                                    onEntered: {
                                                        parent.border.color = "white"; parent.border.width = 1
                                                        rectToolTip.text = modelData.count + " submissions on " + modelData.date
                                                        rectToolTip.visible = true
                                                    }
                                                    onExited: { parent.border.width = 0; rectToolTip.visible = false }
                                                    onPositionChanged: {
                                                        var globalPos = dayRect.mapToItem(window.contentItem, mouseX, mouseY)
                                                        rectToolTip.x = globalPos.x + 12; rectToolTip.y = globalPos.y + 12
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // =========================================================
            // SECTION 3: UPCOMING CONTESTS
            // =========================================================
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 20

                Text {
                    text: "Upcoming Contests"
                    color: "white"; font.pixelSize: 22; font.bold: true
                }

                RowLayout {
                    spacing: 20
                    Layout.fillWidth: true

                    Repeater {
                        model: (typeof contestBackend !== 'undefined' && contestBackend !== null) ? contestBackend.contestModel : []
                        delegate: Item {
                            width: 424; height: 230
                            Rectangle {
                                id: container
                                anchors.fill: parent; radius: 20; color: "#1e1e1e"
                                border.color: hoverArea.containsMouse ? "#ffa116" : "#333"
                                border.width: 1
                                layer.enabled: true
                                layer.effect: OpacityMask {
                                    maskSource: Rectangle { width: container.width; height: container.height; radius: container.radius }
                                }

                                AnimatedImage {
                                    anchors.fill: parent
                                    source: modelData.isWeekly ? "./img/img1.png" : "./img/img2.png"
                                    fillMode: Image.PreserveAspectCrop
                                    playing: hoverArea.containsMouse
                                    opacity: hoverArea.containsMouse ? 0.7 : 0.5
                                }

                                Rectangle {
                                    anchors.fill: parent; radius: 20
                                    gradient: Gradient {
                                        GradientStop { position: 0.3; color: "transparent" }
                                        GradientStop { position: 1.0; color: "#cc000000" }
                                    }
                                }
                            }

                            MouseArea {
                                id: hoverArea
                                anchors.fill: parent; cursorShape: Qt.PointingHandCursor; hoverEnabled: true
                                onClicked: Qt.openUrlExternally("https://leetcode.com/contest/" + modelData.slug + "/")
                            }

                            ColumnLayout {
                                anchors.left: parent.left; anchors.right: parent.right
                                anchors.bottom: parent.bottom; anchors.margins: 25
                                spacing: 8
                                Text { text: modelData.title; color: "white"; font.pixelSize: 22; font.bold: true }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "📅 " + modelData.startTime; color: "#ddd"; font.pixelSize: 14 }
                                    Item { Layout.fillWidth: true }
                                    Text { text: "⏳ " + modelData.duration; color: "#ffa116"; font.pixelSize: 14; font.bold: true }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    ToolTip {
        id: rectToolTip; delay: 0; timeout: -1; closePolicy: Popup.NoAutoClose
        background: Rectangle { color: "#2d2d2d"; radius: 4; border.color: "#444" }
        contentItem: Text { text: rectToolTip.text; color: "white"; font.pixelSize: 12 }
    }
}
