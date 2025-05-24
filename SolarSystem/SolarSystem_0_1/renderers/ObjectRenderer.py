from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPixmap, QFont, QFontMetrics
import math

class ObjectRenderer:
    def __init__(self):
        self.size_changed = 1
        self.texture = QPixmap("SolarSystem_0_1/textures/visibiliti.png")


    def draw_object(self, painter, obj, camera):
        visible_scale = -19 * camera.scale + 20

        pos = obj.get_position()
        base_size = obj.radius * camera.scale
        
        if self.size_changed > 1:
            if obj.radius > 10000000:
                size = base_size * self.size_changed
            else: size = base_size * self.size_changed * self.size_changed
        else:
            size = base_size

        rect = QRectF(
            (pos[0] + camera.offset.x) * camera.scale - size / 2,
            (pos[1] + camera.offset.y) * camera.scale - size / 2,
            size, size
        )

        text_rect = QRectF(
            (pos[0] + camera.offset.x) * camera.scale - size / 2,
            (pos[1] + camera.offset.y) * camera.scale + size / 2, 
            size, size
        )


        if obj.is_visibiliti:
            painter.drawPixmap(rect, self.texture, self.texture.rect())

            font = QFont("Arial", 10)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))

            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(obj.name)
        
            text_rect.setLeft((pos[0] + camera.offset.x) * camera.scale - text_width / 2)
            text_rect.setWidth(text_width)
            text_rect.setTop(text_rect.top() + size)
            text_rect.setHeight(metrics.height())
        
            painter.drawText(text_rect, Qt.AlignBottom | Qt.AlignHCenter, obj.name)

        if not obj.texture.isNull():
            painter.drawPixmap(rect, obj.texture, obj.texture.rect())
        else:
            painter.setBrush(QColor(200, 200, 200))
            painter.drawEllipse(rect)




