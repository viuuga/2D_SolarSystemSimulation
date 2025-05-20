from PySide6.QtCore import QTimer, QPointF, QRectF, QElapsedTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPixmap, QPolygonF
from PySide6.QtWidgets import QWidget
import numpy as np
from space_objects.physicalObject import PhysicalObject
from view.Camera import Camera
from data.LoaderData import Loader


class MainWidget(QWidget):
    def __init__(self, parent=None, filePath: str = None):
        super().__init__(parent)
        self.camera = Camera()
        self.loader = Loader(filePath)
        self.setup_simulation()
        self.setup_visuals()
        
    def setup_simulation(self):
        self.time_acceleration = 1.0
        self.trajectory = []
        self.objects = self.loader.objects

        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.update_positions)
        self.simulation_timer.start(10)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
        self.update_center_point()

    def resizeEvent(self, event):
        self.update_center_point()
        super().resizeEvent(event)

    def update_center_point(self):
        self.center_glob_coords = QPointF(0, 0)
        self.center_screen = QPointF(self.width() / 2, self.height() / 2)

    def setup_visuals(self):
        self.trajectory_length = 1000
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.camera.start_drag(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if self.camera.is_dragging:
            self.camera.drag(event.position().toPoint())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.camera.end_drag()

    def wheelEvent(self, event):
        zoom_factor = 1.1
        mouse_pos = event.position()

        if event.angleDelta().y() > 0:
            self.camera.scale *= zoom_factor
        else:
            self.camera.scale /= zoom_factor
        
        self.update()


    

    def update_positions(self):
        current_time = self.elapsed_timer.elapsed() / 1000.0  # В секундах

        for obj in self.objects:
            obj.update_pos(current_time, self.time_acceleration)

        
        if len(self.objects) > 1: 
            self.update_trajectory(self.objects[1])

        self.update()

    def update_trajectory(self, obj):
        pos = obj.get_position()
        self.trajectory.append((pos[0], pos[1]))  # Используем только X и Y для 2D отрисовки
        if len(self.trajectory) > self.trajectory_length:
            self.trajectory.pop(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_all_objects(painter)
        painter.end()

    def draw_all_objects(self, painter):
        # Применяем трансформации камеры
        painter.translate(self.center_screen)
        painter.scale(self.camera.scale, self.camera.scale)
        painter.translate(self.camera.offset)
        # Рисуем траекторию
        if len(self.trajectory) > 1:
            painter.setPen(QColor(100, 100, 255, 150))
            points = [QPointF(x, y) for x, y in self.trajectory]
            painter.drawPolyline(QPolygonF(points))

        # Рисуем все объекты
        for obj in self.objects:
            self.draw_object(painter, obj)

    def draw_object(self, painter, obj):
        pos = obj.get_position()
        size = max(2, obj.radius * 1000 ** 1/13)
        
        rect = QRectF(
            pos[0] - size / 2,
            pos[1] - size / 2,
            size, size
        )

        if not obj.texture.isNull():
            painter.drawPixmap(rect, obj.texture, obj.texture.rect())
        else:
            painter.setBrush(QColor(200, 200, 200))
            painter.drawEllipse(rect)