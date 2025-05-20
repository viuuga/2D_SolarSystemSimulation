from PySide6.QtCore import QPointF


class Camera:
    def __init__(self):
        self.scale = 0.000000001
        self.offset = QPointF(0, 0)
        self.drag_start_pos = None
        self.is_dragging = False
    
    def start_drag(self, pos):
        self.drag_start_pos = pos
        self.is_dragging = True
    
    def drag(self, pos):
        if self.is_dragging and self.drag_start_pos:
            delta = pos - self.drag_start_pos
            self.offset += delta / self.scale
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