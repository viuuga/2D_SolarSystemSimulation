from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QSlider, QDoubleSpinBox)
import math

class LinearSliderControl(QWidget):  # Переименовал класс для ясности
    """Базовый класс для линейных контролов (скорость/размер)"""
    value_changed = Signal(float)
    
    def __init__(self, min_value, max_value, default_value, label, parent=None):
        super().__init__(parent)
        self.MIN_VALUE = min_value
        self.MAX_VALUE = max_value
        self.DEFAULT_VALUE = default_value
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        slider_layout = QHBoxLayout()
        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(self.value_to_slider_pos(self.DEFAULT_VALUE))
        self.slider.valueChanged.connect(self.on_slider_changed)
        
        slider_layout.addWidget(self.label)
        slider_layout.addWidget(self.slider)
        
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(self.MIN_VALUE, self.MAX_VALUE)
        self.spinbox.setValue(self.DEFAULT_VALUE)
        self.spinbox.setDecimals(3)
        self.spinbox.setSingleStep(0.1)
        self.spinbox.valueChanged.connect(self.on_spinbox_changed)
        
        layout.addLayout(slider_layout)
        layout.addWidget(self.spinbox)
        layout.setContentsMargins(10, 5, 10, 5)

    def value_to_slider_pos(self, value):
        normalized = (value - self.MIN_VALUE) / (self.MAX_VALUE - self.MIN_VALUE)
        return int(normalized * 1000)

    def slider_pos_to_value(self, slider_pos):
        normalized = slider_pos / 1000
        return self.MIN_VALUE + normalized * (self.MAX_VALUE - self.MIN_VALUE)

    def on_slider_changed(self, slider_pos):
        value = self.slider_pos_to_value(slider_pos)
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value)
        self.spinbox.blockSignals(False)
        self.label.setText(f"{self.label.text().split(':')[0]}: {value:.3g}")
        self.value_changed.emit(value)

    def on_spinbox_changed(self, value):
        slider_pos = self.value_to_slider_pos(value)
        self.slider.blockSignals(True)
        self.slider.setValue(slider_pos)
        self.slider.blockSignals(False)
        self.label.setText(f"{self.label.text().split(':')[0]}: {value:.3g}")
        self.value_changed.emit(value)

class SpeedControl(LinearSliderControl):
    def __init__(self, parent=None):
        super().__init__(
            min_value=0.1,
            max_value=400000.0,
            default_value=1.0,
            label="Speed:",
            parent=parent
        )

class SizeControl(LinearSliderControl):
    def __init__(self, parent=None):
        super().__init__(
            min_value=1,
            max_value=35,
            default_value=1.0,
            label="Size:",
            parent=parent
        )

class SpeedWidget(QWidget):
    speed_changed = Signal(float)
    size_changed = Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.size_control = SizeControl()
        self.size_control.value_changed.connect(self.size_changed)
        
        self.speed_control = SpeedControl()
        self.speed_control.value_changed.connect(self.speed_changed)
        
        layout.addWidget(self.size_control)
        layout.addWidget(self.speed_control)