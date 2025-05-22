from PySide6.QtCore import QTimer, QPointF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from multiprocessing import Pool, cpu_count

from simulation.Camera import Camera
from simulation.SimulationEngine import SimulationEngine
from renderers.ObjectRenderer import ObjectRenderer
from renderers.OrbitRenderer import OrbitRenderer
from simulation.SimulationOrbit import SimulationOrbit

class MainWidget(QWidget):
    def __init__(self, parent=None, filePath: str = None):
        super().__init__(parent)
        self.camera = Camera()
        self.last_count = 0
        self.count = 0
        self.main_processe_pool = Pool(processes = max(1, cpu_count() - 2))
        self.background_processe_poll = Pool(processes = 1)
        print(self.main_processe_pool)
        print(self.background_processe_poll)
        
        self.simulation_engine = SimulationEngine(filePath, self.main_processe_pool, self.camera)
        self.orbit_manager = OrbitRenderer(self.simulation_engine.loader.objects)
        self.orbit_simulator = SimulationOrbit()
        self.orbit_simulator.task_completed.connect(self.handle_ellipse_data)
        
        self.setup_ui()
        self.setup_timers()
        
    def setup_ui(self):
        self.setMouseTracking(True)
        self.center_screen = QPointF(self.width() / 2, self.height() / 2)

    def resizeEvent(self, event):
        self.center_screen = QPointF(self.width() / 2, self.height() / 2)
        super().resizeEvent(event)
        
    def setup_timers(self):
        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.update_simulation)
        self.simulation_timer.start(3)

        self.debug_timer = QTimer(self)
        self.debug_timer.timeout.connect(self.debug_output)
        self.debug_timer.start(1000)

        self.update_orbit_timer = QTimer(self)
        self.update_orbit_timer.timeout.connect(self.update_orbit)
        self.update_orbit_timer.start(10000)

        
    def update_simulation(self):
        self.count += 1
        self.simulation_engine.update_positions()
        self.orbit_manager.update_orbits(self.count)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.center_screen)

        self.orbit_manager.draw_orbits(painter, self.camera)
        
        for obj in self.simulation_engine.loader.objects:
              ObjectRenderer.draw_object(painter, obj, self.camera)

        self.orbit_manager.draw_ellipse(painter, self.camera)
            
        painter.end()

    def debug_output(self):
        print(f"fps: {self.count - self.last_count}")
        print(f"{self.camera.offset}")
        self.last_count = self.count

    def update_orbit(self):
        self.orbit_simulator.update_points(self.simulation_engine.loader.objects, self.simulation_engine.loader.objects_dict)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.camera.start_drag(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if self.camera.is_dragging:
            self.simulation_engine.following_object_text = None
            self.camera.drag(event.position().toPoint())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.camera.end_drag()

    def wheelEvent(self, event):
        zoom_factor = 1.1

        if event.angleDelta().y() > 0:
            self.camera.scale *= zoom_factor
        else:
            self.camera.scale /= zoom_factor
        
        self.update()
    
    def closeEvent(self, event):
        self.main_processe_pool.close()
        self.main_processe_pool.join()
        super().closeEvent(event)

    def handle_ellipse_data(self, data):
        self.orbit_manager.ellipses_to_draw = data
        self.update()

