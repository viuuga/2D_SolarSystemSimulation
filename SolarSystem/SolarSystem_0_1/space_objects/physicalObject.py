from typing import List

import numpy as np

from my_math.m_f_file import Vector2d
import math

from PySide6.QtGui import QColor

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import QRectF
from collections import deque

G = 6.67430e-11  # Гравитационная постоянная (Н·м²/кг²)

class PhysicalObject:
    def __init__(self, x: float, y: float, z: float, 
                 velocity: np.ndarray, mass: float, name: str = "",
                 texture_path: str = "SolarSystem_0_1/textures/none_texture.png", 
                 radius: int = 10000000000):
        self.name = name
        self.position = np.array([x, y, z], dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.acceleration = np.zeros(3)
        self.last_acceleration = np.zeros(3)
        self.last_update_time = 0.0
        self.texture_path = texture_path
        self._texture = None
        self.gravitation_influences = []
        self.radius = radius
        self.orbit_history = deque(maxlen=100)
        self.orbit_color = self._generate_orbit_color()

    @property
    def texture(self):
        if self._texture is None:
            self._texture = QPixmap(self.texture_path)
            if self._texture.isNull():
                self._texture = QPixmap("SolarSystem_0_1/textures/none_texture.png")
        return self._texture

    def get_position(self) -> np.ndarray:
        return self.position.copy()

    def get_mass(self) -> float:
        return self.mass

    def to_dict(self):
        """Конвертирует объект в словарь для передачи в процессы"""
        return {
            'position': self.position.tolist(),
            'velocity': self.velocity.tolist(),
            'acceleration': self.acceleration.tolist(),
            'last_acceleration': self.last_acceleration.tolist(),
            'last_update_time': self.last_update_time,
            'mass': self.mass,
            'gravitation_influences': [
                {
                    'position': obj.position.tolist(),
                    'mass': obj.mass
                } 
                for obj in self.gravitation_influences
            ]
        }

    def from_dict(self, data: dict):
        """Обновляет объект из словаря"""
        self.position = np.array(data['position'])
        self.velocity = np.array(data['velocity'])
        self.acceleration = np.array(data['acceleration'])
        self.last_acceleration = np.array(data['last_acceleration'])
        self.last_update_time = data['last_update_time']

    def add_gravitational_influence(self, obj: 'PhysicalObject'):
        if obj not in self.gravitation_influences:
            self.gravitation_influences.append(obj)

    def _generate_orbit_color(self):
        hash_val = hash(self.name) % 0xFFFFFF
        return QColor(hash_val >> 16, (hash_val >> 8) & 0xFF, hash_val & 0xFF)