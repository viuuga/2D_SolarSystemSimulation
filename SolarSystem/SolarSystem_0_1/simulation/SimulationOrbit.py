from PySide6.QtCore import QThread, Signal
import numpy as np

class SimulationOrbit(QThread):
    task_completed = Signal(dict)

    def __init__(self):
        super().__init__()
        self.orbit_data = {}
        self.ellipse_data = {}

    def update_points(self, objects, object_dict):
        self.orbit_data = {}
        
        for obj in objects:
            if not hasattr(obj, 'orbit_history') or len(obj.orbit_history) < 3 or obj.center_name == "" or obj.obType == "moon":
                continue

            p1 = np.array(obj.position, dtype=np.float64) / 1e8
            p2 = np.array(obj.orbit_history[len(obj.orbit_history)//2], dtype=np.float64) / 1e8
            p3 = np.array(obj.orbit_history[0], dtype=np.float64) / 1e8
                   
            center = np.array(object_dict.get(obj.center_name).position, dtype=np.float64) / 1e8
            

            self.orbit_data[obj.name] = {
                'points': [p1, p2, p3],
                'center': center,
                'color': getattr(obj, 'orbit_color', (255, 255, 255))
            }

        self.start()

    def run(self):
        results = {}
        
        for name, data in self.orbit_data.items():
            equation = self._calculate_ellipse_equation(
                data['points'], 
                data['center']
            )
            
            if equation:
                segments = self._generate_ellipse_points(equation, data['center'])
                results[name] = {
                    'points': segments,
                    'color': data['color'],
                    'center': data['center']
                }

        self.task_completed.emit(results)

    def _calculate_ellipse_equation(self, points, center):
        try:
            p1, p2, p3 = [point - center for point in points]
            
            M = np.array([
                [p1[0]**2, p1[0]*p1[1], p1[1]**2],
                [p2[0]**2, p2[0]*p2[1], p2[1]**2],
                [p3[0]**2, p3[0]*p3[1], p3[1]**2]
            ])

            print(p1, p2, p3)
            
            v = np.array([1.0, 1.0, 1.0])
            
            A, B, C = np.linalg.solve(M, v)

            if B**2 - 4*A*C >= 0:
                print(f"Hyperbola detected: A={A}, B={B}, C={C}, discriminant={B**2-4*A*C}")
                print(f"Points: {points}")
                print(f"Center: {center}")
                return None

            return {'A': A, 'B': B, 'C': C}
            
        except np.linalg.LinAlgError:
            print("np.linalg.LinAlgError")
            return None

    def _generate_ellipse_points(self, equation, center, num_points=100):
        A, B, C = equation['A'], equation['B'], equation['C']
        points = []
        
        for i in range(num_points + 1):
            theta = 2 * np.pi * i / num_points
            x = np.cos(theta)
            y = np.sin(theta)
            
            denominator = A*x**2 + B*x*y + C*y**2
            if denominator <= 1e-10:
                continue
                
            r = 1.0 / np.sqrt(denominator)
            px = center[0] + r * x
            py = center[1] + r * y
            points.append((px, py))
            
        return points