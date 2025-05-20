from typing import List

import numpy as np

from my_math.m_f_file import Vector2d
import math

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import QRectF

G =  6.67430e-11  # Гравитационная постоянная (Н·м²/кг²)

class PhysicalObject:
    def __init__(
        self,
        x: float,   #метры
        y: float,   #метры
        z: float,   #метры
        velocity: np.ndarray,  # [vx, vy, vz]
        mass: float,   #килограммы
        name: str = "",
        texture_path: str = "SolarSystem_0_1/textures/none_texture.png",
        radius: int = 10000000000,  #метры
    ):
        self.name = name
        self.position = np.array([x, y, z], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.acceleration = np.zeros(3)  # 3D ускорение

        self.last_update_time = 0.0
        self.texture_path = texture_path
        self.texture = QPixmap(texture_path)
        if self.texture.isNull():
            self.texture = QPixmap("SolarSystem_0_1/textures/none_texture.png")
            self.texture_path = "SolarSystem_0_1/textures/none_texture.png"

        self.gravitation_influences: List[PhysicalObject] = []
        self.radius = radius

    def get_position(self) -> np.ndarray:
        return self.position.copy()

    def get_mass(self) -> float:
        return self.mass

    def update_pos(self, current_time: float, time_acceleration: float):
        delta_time = (current_time - self.last_update_time) * time_acceleration

        if delta_time <= 0:
            return
        if delta_time > 5000:  # Защита от слишком больших шагов
            delta_time = 5000

        # Если нет гравитационных влияний, просто двигаемся по инерции
        if not self.gravitation_influences:
            self.position += self.velocity * delta_time
            self.last_update_time = current_time
            return

        # Собираем данные всех влияющих тел
        positions = np.array([obj.position for obj in self.gravitation_influences])
        masses = np.array([obj.mass for obj in self.gravitation_influences])

        # Вычисляем ускорение
        self.acceleration = self._calculate_gravity(positions, masses)

        # Обновляем скорость и позицию (интегрируем методом Эйлера)
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time

        self.last_update_time = current_time

    def _calculate_gravity(self, other_positions: np.ndarray, other_masses: np.ndarray) -> np.ndarray:
        """
        Вычисляет гравитационное ускорение, вызванное другими телами.

        Args:
            other_positions (np.ndarray): Массив позиций других тел (shape: [n_bodies, 3]).
            other_masses    (np.ndarray): Массив масс  других  тел  (shape: [n_bodies]).

        Returns:
            np.ndarray: Вектор ускорения (shape: [3]).
        """
        r_vecs = other_positions - self.position    # Векторы от текущего тела к другим
        distances = np.linalg.norm(r_vecs, axis=1)  # Расстояния до других тел

        # Игнорируем нулевые расстояния (чтобы избежать деления на 0)
        mask = distances > 1e-10
        r_vecs = r_vecs[mask]
        distances = distances[mask]
        other_masses = other_masses[mask]

        if len(distances) == 0:
            return np.zeros(3)

        # Сила гравитации (F = G * m1 * m2 / r^2)
        force_magnitudes = G * self.mass * other_masses / (distances ** 2)

        # Направление силы (нормализованные векторы)
        force_dirs = r_vecs / distances[:, np.newaxis]

        # Суммарное ускорение (a = F / m)
        total_acceleration = np.sum(force_magnitudes[:, np.newaxis] * force_dirs, axis=0) / self.mass

        return total_acceleration

    def add_gravitational_influence(self, obj: 'PhysicalObject'):
        """Добавляет объект, который будет влиять на гравитацию."""
        if obj not in self.gravitation_influences:
            self.gravitation_influences.append(obj)