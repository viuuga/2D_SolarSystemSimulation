from PySide6.QtCore import QElapsedTimer

from my_math.PhysicsEngine import PhysicsEngine
from my_math.Point import Point
from data.LoaderData import Loader

class SimulationEngine:
    def __init__(self, filePath, pool, camera):
        self.pool = pool
        self.time_acceleration = 1.0
        self.following_object_text = None
        self.camera = camera
        self.loader = Loader(filePath)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

    
    def update_positions(self):
        if self.following_object_text is not None:
            foloving_object = self.loader.objects_dict.get(self.following_object_text)
            if foloving_object:
                self.camera.offset = Point(-foloving_object.position[0], -foloving_object.position[1])

        current_time = self.elapsed_timer.elapsed() / 1000.0
        objects_data = [obj.to_dict() for obj in self.loader.objects]
        tasks = [(data, current_time, self.time_acceleration) for data in objects_data]
        
        try:
            results = self.pool.starmap(PhysicsEngine.update_position, tasks)
            for obj, result in zip(self.loader.objects, results):
                obj.from_dict(result)
        except Exception as e:
            print(f"Parallel computation failed: {e}")
            for obj, data in zip(self.loader.objects, objects_data):
                result = PhysicsEngine.update_position(data, current_time, self.time_acceleration)
                obj.from_dict(result)