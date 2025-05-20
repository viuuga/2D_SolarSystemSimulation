from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSlider, QMenuBar


class SpeedWidget(QWidget):
    speed_changed = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        control_layout = QHBoxLayout()
        self.setLayout(control_layout)

        self.speed_label = QLabel("speed: 10000x")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000000)
        self.speed_slider.setValue(10000)
        self.speed_slider.setFixedWidth(200)
        self.speed_slider.valueChanged.connect(self.update_simulation_speed)

        control_layout.addWidget(QLabel("speed:"))
        control_layout.addWidget(self.speed_slider)
        control_layout.addWidget(self.speed_label)
        control_layout.setContentsMargins(10, 0, 10, 0)

    def update_simulation_speed(self, value):
        self.speed_label.setText(f"speed: {value}x")
        self.speed_changed.emit(value)



