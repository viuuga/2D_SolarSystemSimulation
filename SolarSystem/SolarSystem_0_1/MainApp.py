from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSlider, QMenuBar, QDockWidget


from interface.SpeedSlider import SpeedWidget
from interface.ObjectsPanel import ObjectsPanel
from mainWidget.MainWidget import MainWidget
from interface.SettingsPanel import SettingsPanel
from data.LoaderData import Loader


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setWindowTitle("Solar system")
        self.loader = Loader()
        
        self.mainWidget = MainWidget(self.loader, self)
        self.setCentralWidget(self.mainWidget)
        
        self.objects_panel = ObjectsPanel(self.loader, self)

        self.settings_panel = SettingsPanel( self.loader, self)
        self.settings_dock = QDockWidget("Настройки", self)
        self.settings_dock.setWidget(self.settings_panel)
        self.settings_dock.setFeatures(QDockWidget.DockWidgetClosable)
        self.settings_dock.hide()
        self.addDockWidget(Qt.RightDockWidgetArea, self.settings_dock)
        
        self.add_menu_and_controls()

    def add_menu_and_controls(self):
        menu_container = QWidget()
        menu_layout = QHBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction("Настройки", self.toggle_settings_panel)
        file_menu.addAction("Выход")
        
        objects_action = file_menu.addAction("Объекты")
        objects_action.triggered.connect(self.objects_panel.toggle_panel)
        self.objects_panel.object_changed.connect(self.handle_object_change)
        
        self.control_widget = SpeedWidget(self)
        self.control_widget.speed_changed.connect(self.handle_speed_change)
        self.control_widget.size_changed.connect(self.handle_size_change)
        
        menu_layout.addWidget(menu_bar)
        menu_layout.addStretch()
        menu_layout.addWidget(self.control_widget)

        self.setMenuWidget(menu_container)

    def toggle_settings_panel(self):
        self.settings_dock.setVisible(not self.settings_dock.isVisible())

    def handle_speed_change(self, value):
        self.mainWidget.simulation_engine.time_acceleration = value

    def handle_size_change(self, value):
        self.mainWidget.object_renderer.size_changed = value
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.objects_panel.setFixedHeight(self.height())

    def handle_object_change(self, value):
        print(f"Объект выбран: {value}")
        self.mainWidget.simulation_engine.following_object_text = value

if __name__ == "__main__":
    app = QApplication()
    widget = MainApp()
    widget.show()
    app.exec()