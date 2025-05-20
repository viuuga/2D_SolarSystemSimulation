from PySide6.QtWidgets import (QScrollArea, QVBoxLayout, QPushButton, 
                              QListWidget, QListWidgetItem, QFrame, QLabel, QWidget, QHBoxLayout)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPoint
from PySide6.QtGui import QIcon

class ObjectsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(200)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border-right: 1px solid #ccc;
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Заголовок и кнопка закрытия
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel("Объекты")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_btn.clicked.connect(self.hide_panel)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        
        # Список объектов
        self.objects_list = QListWidget()
        self.objects_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background: #e0e0e0;
            }
        """)
        
        layout.addWidget(header)
        layout.addWidget(self.objects_list)
        
        self.add_sample_objects()
        
    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.hide_panel(immediate=True)
        
    def add_sample_objects(self):
        objects = [
            ("Солнце", ":/icons/sun.png"),
            ("Меркурий", ":/icons/mercury.png"),
            ("Венера", ":/icons/venus.png"),
            ("Земля", ":/icons/earth.png"),
            # Добавьте другие объекты по аналогии
        ]
        
        for name, icon_path in objects:
            item = QListWidgetItem(QIcon(icon_path), name)
            item.setFlags(item.flags() | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.objects_list.addItem(item)
        
        self.objects_list.itemClicked.connect(self.on_object_clicked)
    
    def on_object_clicked(self, item):
        print(f"Объект выбран: {item.text()}")
        # Здесь можно добавить логику взаимодействия с главным виджетом
        
    def toggle_panel(self):
        if self.x() < 0:
            self.show_panel()
        else:
            self.hide_panel()
    
    def show_panel(self):
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(0, 0))
        self.animation.start()
    
    def hide_panel(self, immediate=False):
        if immediate:
            self.move(-self.width(), 0)
        else:
            self.animation.setStartValue(self.pos())
            self.animation.setEndValue(QPoint(-self.width(), 0))
            self.animation.start()
    
    def resizeEvent(self, event):
        self.setFixedHeight(self.parent.height())
        super().resizeEvent(event)



