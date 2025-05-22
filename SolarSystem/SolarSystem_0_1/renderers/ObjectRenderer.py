from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor


class ObjectRenderer:
    @staticmethod
    def draw_object(painter, obj, camera):
        pos = obj.get_position()
        size = (obj.radius * 3200 ** (1/19) * camera.scale)
        
        rect = QRectF(
            (pos[0] + camera.offset.x) * camera.scale - size / 2,
            (pos[1] + camera.offset.y) * camera.scale - size / 2,
            size, size
        )

        if not obj.texture.isNull():
            painter.drawPixmap(rect, obj.texture, obj.texture.rect())
        else:
            painter.setBrush(QColor(200, 200, 200))
            painter.drawEllipse(rect)




