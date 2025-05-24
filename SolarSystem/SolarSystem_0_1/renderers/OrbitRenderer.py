from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPolygonF, QPen, QColor, QPainterPath
import numpy as np

class OrbitRenderer:
    def __init__(self, objects, objects_dict):
        self.objects = objects
        self.objects_dict = objects_dict
        self.ellipses_to_draw = {} 
        
    def update_orbits(self, count, time_acceleration):
        delimater = 35 - 30 * time_acceleration // 400000
        if count % delimater == 0:
            for obj in self.objects:
                obj.orbit_history.append(obj.position.copy())
    
    def draw_orbits(self, painter, camera):
        
        base_pen = QPen()
        base_pen.setWidthF(1.0)
        
        for obj in self.objects:
            if len(obj.orbit_history) < 2 or not obj.is_simulate_traectory:
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
            if not self.objects_dict.get(ellipse['object']).is_simulate_orbit:
                continue
            
            painter.setPen(QPen(QColor(ellipse['color']), 1))
            painter.setBrush(Qt.NoBrush)


            center = (np.array(self.objects_dict.get(ellipse['center_name']).position, dtype=np.float64) + np.array(self.objects_dict.get(ellipse['object']).center_orbit, dtype=float))
        
            path = QPainterPath()
            x, y = ellipse['points'][0]
            path.moveTo(
                (x * ellipse['scale'] + camera.offset.x + center[0]) * camera.scale,
                (y * ellipse['scale'] + camera.offset.y + center[1]) * camera.scale
            )
        
            for x, y in ellipse['points'][1:]:
                path.lineTo(
                    (x * ellipse['scale'] + camera.offset.x + center[0]) * camera.scale,
                    (y * ellipse['scale'] + camera.offset.y + center[1]) * camera.scale
                )
            
            painter.drawPath(path)


