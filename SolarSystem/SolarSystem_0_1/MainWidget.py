from PySide6.QtCore import QTimer, QPointF, QRectF, QElapsedTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QPolygonF
from PySide6.QtWidgets import QWidget
import json
import numpy as np
from space_objects.physicalObject import PhysicalObject


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_simulation()
        self.setup_visuals()
        self.load_solar_system("SolarSystem_0_1/data/SolarSystem.json")

    def setup_simulation(self):
        self.time_acceleration = 1.0
        self.trajectory = []
        self.objects = []

        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.update_positions)
        self.simulation_timer.start(10)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

    def setup_visuals(self):
        self.scale = 1.0
        self.center_offset = QPointF(0, 0)
        self.trajectory_length = 1000
        self.setMouseTracking(True)

    def load_solar_system(self, json_path):
        try:
            with open(json_path) as f:
                data = json.load(f)

            # Создаём Солнце
            sun = self.create_physical_object(data['sun'])
            self.objects.append(sun)

            # Создаём планеты и их спутники
            for planet_name, planet_data in data.get('planets', {}).items():
                planet = self.create_physical_object(planet_data)
                self.objects.append(planet)
                planet.gravitation_influences.append(sun)
                sun.gravitation_influences.append(planet)

                # Обрабатываем спутники
                for moon_name, moon_data in planet_data.get('satellites', {}).items():
                    moon = self.create_moon_object(moon_data, planet)
                    self.objects.append(moon)
                    moon.gravitation_influences.extend([planet, sun])
                    planet.gravitation_influences.append(moon)

        except Exception as e:
            print(f"Error loading solar system: {e}")

    def create_physical_object(self, obj_data):
        return PhysicalObject(
            x=obj_data['x'],
            y=obj_data['y'],
            z=obj_data.get('z', 0),
            velocity=np.array(obj_data['velocity']),
            mass=obj_data['mass'],
            texture_path=obj_data['texture'],
            radius=obj_data['radius']
        )

    def create_moon_object(self, moon_data, parent_planet):
        # Позиция спутника относительно планеты
        offset = np.array(moon_data['offset'])
        position = parent_planet.position + offset

        # Скорость спутника = скорость планеты + орбитальная скорость
        velocity = parent_planet.velocity + np.array(moon_data['velocity'])

        return PhysicalObject(
            x=position[0],
            y=position[1],
            z=position[2],
            velocity=velocity,
            mass=moon_data['mass'],
            texture_path=moon_data['texture'],
            radius=moon_data['radius']
        )

    def update_positions(self):
        current_time = self.elapsed_timer.elapsed() / 1000.0  # В секундах

        for obj in self.objects:
            obj.update_pos(current_time, self.time_acceleration)

        # Сохраняем траекторию Земли (для примера)
        if len(self.objects) > 1:  # Земля обычно второй объект
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
        center = QPointF(self.width() / 2, self.height() / 2)
        self.scale = min(self.width(), self.height()) / 3_000_000_000_00  # Масштаб для визуализации

        # Рисуем траекторию
        if len(self.trajectory) > 1:
            painter.setPen(QColor(100, 100, 255, 150))
            points = [QPointF(
                center.x() + x * self.scale,
                center.y() + y * self.scale
            ) for x, y in self.trajectory]
            painter.drawPolyline(QPolygonF(points))

        # Рисуем все объекты
        for obj in self.objects:
            self.draw_object(painter, obj, center)

    def draw_object(self, painter, obj, center):
        pos = obj.get_position()
        screen_pos = QPointF(
            center.x() + pos[0] * self.scale,
            center.y() + pos[1] * self.scale
        )

        size = obj.radius **(1/3) / 20
        rect = QRectF(
            screen_pos.x() - size / 2,
            screen_pos.y() - size / 2,
            size, size
        )

        # Рисуем текстуру
        if not obj.texture.isNull():
            painter.drawPixmap(rect, obj.texture, obj.texture.rect())
        else:
            painter.setBrush(QColor(200, 200, 200))
            painter.drawEllipse(rect)
