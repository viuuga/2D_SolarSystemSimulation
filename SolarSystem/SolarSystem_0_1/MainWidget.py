from PySide6.QtCore import QPoint, QTimer, QPointF, QRectF, QElapsedTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPixmap, QPolygonF, QPen
from PySide6.QtWidgets import QWidget
import numpy as np
from space_objects.physicalObject import PhysicalObject
from view.Camera import Camera
from data.LoaderData import Loader
from my_math.Point import Point
from my_math.PhysicsEngine import PhysicsEngine
from multiprocessing import Pool, cpu_count

class MainWidget(QWidget):
    def __init__(self, parent=None, filePath: str = None):
        super().__init__(parent)
        self.camera = Camera()
        self.loader = Loader(filePath)
        self.pool = Pool(processes=cpu_count()) 
        self.orbits = {}
        self.show_full_orbits = True
        self.setup_simulation()
        self.setup_visuals()
        
    def setup_simulation(self):
        self.time_acceleration = 1.0
        self.trajectory = []
        self.objects = self.loader.objects
        self.foloving_object_text = None
        self.foloving_object = None

        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.update_positions)
        self.simulation_timer.start(3)

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
            self.foloving_object_text = None
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
        current_time = self.elapsed_timer.elapsed() / 1000.0
        
        if self.foloving_object_text is not None:
            self.foloving_object = self.loader.objects_dict.get(self.foloving_object_text)
            self.camera.offset = Point(-self.foloving_object.position[0], 
                                     -self.foloving_object.position[1])

        # Подготавливаем данные для процессов
        tasks = [(obj.to_dict(), current_time, self.time_acceleration) 
                for obj in self.objects]
        
        try:
            results = self.pool.starmap(PhysicsEngine.update_position, tasks)
            
            # Обновляем объекты из результатов
            for obj, result in zip(self.objects, results):
                obj.from_dict(result)
                
        except Exception as e:
            print(f"Parallel computation failed: {e}")
            # Резервный последовательный расчет
            for obj in self.objects:
                data = PhysicsEngine.update_position(
                    obj.to_dict(), current_time, self.time_acceleration
                )
                obj.from_dict(data)
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_all_objects(painter)
        painter.end()

    def draw_all_objects(self, painter):
        print(f"{self.camera.offset}")
        # Применяем трансформации камеры
        painter.translate(self.center_screen)
        painter.scale(self.camera.scale, self.camera.scale)

 
        # Рисуем все объекты
        for obj in self.objects:
            self.draw_object(painter, obj)
        

    def draw_object(self, painter, obj):
        pos = obj.get_position()
        size = max(2, obj.radius * 1000 ** 1/13)
        
        rect = QRectF(
            pos[0] + self.camera.offset.x - size / 2,
            pos[1] + self.camera.offset.y - size / 2,
            size, size
        )

        if not obj.texture.isNull():
            painter.drawPixmap(rect, obj.texture, obj.texture.rect())
        else:
            painter.setBrush(QColor(200, 200, 200))
            painter.drawEllipse(rect)

    def closeEvent(self, event):
        self.pool.close()
        self.pool.join()
        super().closeEvent(event)