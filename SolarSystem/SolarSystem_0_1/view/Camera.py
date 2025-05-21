from PySide6.QtCore import QPointF
from my_math.Point import Point

class Camera:
    def __init__(self):
        self.scale = 0.000000001
        self.offset = Point()
        self.drag_start_pos = None
        self.is_dragging = False
    
    def start_drag(self, pos):
        self.drag_start_pos = pos
        print(self.drag_start_pos)
        self.is_dragging = True
    
    def drag(self, pos):
        if self.is_dragging and self.drag_start_pos:
            delta = Point(pos.x() - self.drag_start_pos.x(), 
                         pos.y() - self.drag_start_pos.y())
        
            # Масштабируем дельту с проверкой на слишком большие значения
            scaled_delta = delta / self.scale
        
            # Проверка на разумные пределы (эмпирические значения)
            max_offset = 1e15  # Максимальное абсолютное значение координаты
            new_offset = self.offset + scaled_delta
        
            if abs(new_offset.x) < max_offset and abs(new_offset.y) < max_offset:
                self.offset = new_offset
            else:
                # Обработка случая переполнения - можно сбросить или ограничить
                self.offset = Point(
                    max(-max_offset, min(max_offset, new_offset.x)),
                    max(-max_offset, min(max_offset, new_offset.y))
                )
            self.drag_start_pos = pos
    
    def end_drag(self):
        self.is_dragging = False
        self.drag_start_pos = None
    
    def apply_transform(self, painter):
        painter.scale(self.scale, self.scale)
    
    def screen_to_world(self, screen_point, center_screen):
        return (screen_point - center_screen - self.offset) / self.scale
    
    def world_to_screen(self, world_point, center_screen):
        return world_point * self.scale + self.offset + center_screen