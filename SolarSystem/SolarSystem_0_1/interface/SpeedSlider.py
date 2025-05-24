from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QSlider, QDoubleSpinBox)
import math

class LogSliderControl(QWidget):
    """Базовый класс для логарифмических контролов (скорость/размер)"""
    value_changed = Signal(float)
    
    def __init__(self, min_value, max_value, default_value, label, parent=None):
        super().__init__(parent)
        self.MIN_VALUE = min_value
        self.MAX_VALUE = max_value
        self.DEFAULT_VALUE = default_value
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Слайдер
        slider_layout = QHBoxLayout()
        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(self.value_to_slider_pos(self.DEFAULT_VALUE))
        self.slider.valueChanged.connect(self.on_slider_changed)
        
        slider_layout.addWidget(self.label)
        slider_layout.addWidget(self.slider)
        
        # Спинбокс
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(self.MIN_VALUE, self.MAX_VALUE)
        self.spinbox.setValue(self.DEFAULT_VALUE)
        self.spinbox.setDecimals(9)
        self.spinbox.setSingleStep(0.1)
        self.spinbox.valueChanged.connect(self.on_spinbox_changed)
        
        layout.addLayout(slider_layout)
        layout.addWidget(self.spinbox)
        layout.setContentsMargins(10, 5, 10, 5)

    def value_to_slider_pos(self, value):
        """Преобразует значение в позицию слайдера"""
        if value <= 0:
            return 0
        min_log = math.log10(self.MIN_VALUE)
        max_log = math.log10(self.MAX_VALUE)
        log_value = math.log10(value)
        slider_pos = (log_value - min_log) / (max_log - min_log) * 1000
        return int(slider_pos)

    def slider_pos_to_value(self, slider_pos):
        """Преобразует позицию слайдера в значение"""
        min_log = math.log10(self.MIN_VALUE)
        max_log = math.log10(self.MAX_VALUE)
        log_value = min_log + (max_log - min_log) * (slider_pos / 1000)
        return 10 ** log_value

    def on_slider_changed(self, slider_pos):
        """Обработчик изменения слайдера"""
        value = self.slider_pos_to_value(slider_pos)
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value)
        self.spinbox.blockSignals(False)
        self.label.setText(f"{self.label.text().split(':')[0]}: {value:.3g}")
        self.value_changed.emit(value)

    def on_spinbox_changed(self, value):
        """Обработчик изменения спинбокса"""
        slider_pos = self.value_to_slider_pos(value)
        self.slider.blockSignals(True)
        self.slider.setValue(slider_pos)
        self.slider.blockSignals(False)
        self.label.setText(f"{self.label.text().split(':')[0]}: {value:.3g}")
        self.value_changed.emit(value)

class SpeedControl(LogSliderControl):
    """Контрол скорости"""
    def __init__(self, parent=None):
        super().__init__(
            min_value=1e-9,
            max_value=2e5,
            default_value=1.0,
            label="Speed:",
            parent=parent
        )

class SizeControl(LogSliderControl):
    """Контрол размера"""
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
        