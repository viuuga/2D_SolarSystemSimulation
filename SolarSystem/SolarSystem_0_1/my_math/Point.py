


class Point():
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    # Сложение (+)
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Point(self.x + other, self.y + other, self.z + other)
        return NotImplemented
    
    # Вычитание (-)
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Point(self.x - other, self.y - other, self.z - other)
        return NotImplemented
    
    # Умножение (*)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other, self.z * other)
        return NotImplemented
    
    # Деление (/)
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other, self.z / other)
        return NotImplemented
    
    # Отрицание (-)
    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)
    
    # Представление в виде строки
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"
    
    # Преобразование в QPointF (если нужно)
    def to_qpointf(self):
        from PySide6.QtCore import QPointF
        return QPointF(self.x, self.y)
    
    # Проверка на равенство (==)
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False








