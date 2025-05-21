from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QLabel, QSlider, QMenuBar,
                               QSizePolicy)

from MainWidget import MainWidget
from interface.SpeedSlider import SpeedWidget
from interface.ObjectsPanel import ObjectsPanel


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setWindowTitle("Solar system")
        
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        self.objects_panel = ObjectsPanel(self)
        
        self.add_menu_and_controls()

    def add_menu_and_controls(self):
        menu_container = QWidget()
        menu_layout = QHBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction("Настройки")
        file_menu.addAction("Выход")
        
        objects_action = file_menu.addAction("Объекты")
        objects_action.triggered.connect(self.objects_panel.toggle_panel)
        self.objects_panel.object_changed.connect(self.handle_object_change)
        
        self.control_widget = SpeedWidget(self)
        self.control_widget.speed_changed.connect(self.handle_speed_change)
        
        menu_layout.addWidget(menu_bar)
        menu_layout.addStretch()
        menu_layout.addWidget(self.control_widget)

        self.setMenuWidget(menu_container)

    def handle_speed_change(self, value):
        self.mainWidget.time_acceleration = value
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'objects_panel'):
            self.objects_panel.setFixedHeight(self.height())

    def handle_object_change(self, value):
        print(f"Объект выбран: {value}")
        self.mainWidget.foloving_object_text = value


if __name__ == "__main__":
    app = QApplication()
    widget = MainApp()
    widget.show()
    app.exec()