from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPolygonF, QPen, QColor, QPainterPath


class OrbitRenderer:
    def __init__(self, objects):
        self.objects = objects
        self.show_full_orbits = True
        self.ellipses_to_draw = {} 
        
    def update_orbits(self, count):
        if count % 3 == 0:
            for obj in self.objects:
                obj.orbit_history.append(obj.position.copy())
    
    def draw_orbits(self, painter, camera):
        if not self.show_full_orbits:
            return
        
        base_pen = QPen()
        base_pen.setWidthF(1.0)
        
        for obj in self.objects:
            if len(obj.orbit_history) < 2:
                continue

            base_pen.setColor(obj.orbit_color)
            painter.setPen(base_pen)
            
            step = max(1, len(obj.orbit_history) // 100)
            points = QPolygonF()
            for i in range(0, len(obj.orbit_history), step):
                pos = obj.orbit_history[i]
                points.append(QPointF(
                    (pos[0] + camera.offset.x) * camera.scale,
                    (pos[1] + camera.offset.y) * camera.scale
                ))
            if points.size() >= 2:
                painter.drawPolyline(points)

    def draw_ellipse(self, painter, camera):
        for name, ellipse in self.ellipses_to_draw.items():
            if not ellipse['points']:
                continue
            
            painter.setPen(QPen(QColor(ellipse['color']), 1))
            painter.setBrush(Qt.NoBrush)
        
            path = QPainterPath()
            x, y = ellipse['points'][0]
            path.moveTo(
                (x * 1e8 + camera.offset.x) * camera.scale,
                (y * 1e8 + camera.offset.y) * camera.scale
            )
        
            for x, y in ellipse['points'][1:]:
                path.lineTo(
                    (x * 1e8 + camera.offset.x) * camera.scale,
                    (y * 1e8 + camera.offset.y) * camera.scale
                )
            
            painter.drawPath(path)


