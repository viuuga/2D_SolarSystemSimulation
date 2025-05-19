from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QHBoxLayout, QLabel, QSlider, QMenuBar,
                               QSizePolicy)

from MainWidget import MainWidget



class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setWindowTitle("Solar system")
        self.add_menu()

        mainWidget = MainWidget(self)
        self.setCentralWidget(mainWidget)

    def add_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        menu_container = QWidget()
        menu_layout = QHBoxLayout()
        menu_container.setLayout(menu_layout)

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction("Настройки")
        file_menu.addAction("Выход")

        control_widget = QWidget()
        control_layout = QHBoxLayout()
        control_widget.setLayout(control_layout)

        self.speed_label = QLabel("Скорость: 10000x")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000000)
        self.speed_slider.setValue(10000)
        self.speed_slider.setFixedWidth(200)
        self.speed_slider.valueChanged.connect(self.update_simulation_speed)

        control_layout.addWidget(QLabel("Скорость:"))
        control_layout.addWidget(self.speed_slider)
        control_layout.addWidget(self.speed_label)
        control_layout.setContentsMargins(10, 0, 10, 0)


        menu_layout.addWidget(menu_bar, stretch=1)
        menu_layout.addWidget(control_widget, stretch=1)


        self.setMenuWidget(menu_container)

    def update_simulation_speed(self, value):
        self.speed_label.setText(f"Скорость: {value:.2f}x")

        if hasattr(self, 'centralWidget'):
            self.centralWidget().time_acceleration = value


if __name__ == "__main__":
    app = QApplication()
    widget = MainApp()
    widget.show()
    app.exec()