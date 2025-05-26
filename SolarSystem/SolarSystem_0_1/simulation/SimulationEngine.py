from PySide6.QtCore import QElapsedTimer, QThread, Signal

from my_math.PhysicsEngine_v2 import PhysicsEngine2
from my_math.PhysicsEngine import PhysicsEngine
from my_math.Point import Point

class SimulationEngine(QThread):
    task_completed = Signal(bool)

    def __init__(self,pool, camera, loader):
        super().__init__()
        self.pool = pool
        self.time_acceleration = 1
        self.following_object_text = None
        self.camera = camera
        self.loader = loader
        self.is_shoud_update = True
        self.delta_time = 0
        self.fps_count = 0
        self.last_fps_count = 0
        self.last_time = 0

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
        self.last_time_update = self.elapsed_timer.elapsed()
    
    def update_positions2(self):
        self.is_shoud_update = False

        self.delta_time = (self.elapsed_timer.elapsed() - self.last_time_update) * self.time_acceleration / 1000
        self.last_time_update = self.elapsed_timer.elapsed()

        if self.delta_time > 4000:
            self.delta_time = 4000

        self.start()


    def run(self):
        max_substep = 200
        substeps_count = max(1, int(self.delta_time / max_substep))
        substep_time = self.delta_time / substeps_count


        while(substeps_count != 0):
            self.fps_count += 1
            substeps_count -= 1

            list(map(lambda obj: PhysicsEngine2.update_position(obj, substep_time), self.loader.objects))


            if self.following_object_text is not None:
                foloving_object = self.loader.objects_dict.get(self.following_object_text)
                if foloving_object:
                    self.task_completed.emit(True)
                    self.camera.offset = Point(-foloving_object.position[0], -foloving_object.position[1])


        #print((self.elapsed_timer.elapsed() - self.last_time_update) / 1000, " секунд")
        self.task_completed.emit(True)

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