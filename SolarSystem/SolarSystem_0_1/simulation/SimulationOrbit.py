from turtle import update
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QColor
import numpy as np


class SimulationOrbit(QThread):
    task_completed = Signal(dict)

    def __init__(self, objects, object_dict):
        super().__init__()
        self.objects = objects
        self.object_dict = object_dict

    def update_points2(self):
        self.orbit_data = {}
        
        for obj in self.objects:

            if obj.obType == "star" or obj.is_simulate_orbit == False:
                continue


            new_vec = obj.position - self.object_dict.get(obj.center_name).position


            if(abs(angle_between_vectors(new_vec, obj.last_central_vector)) >= 1):
                obj.last_central_vector = new_vec
                obj.orbit_points.append(new_vec.copy())

            if obj.obType== 'moon':
                scale = 1e5
            else: scale = 1e8

            

            if len(obj.orbit_points) != 3:
                p1 = (np.array(obj.position, dtype=np.float64) - np.array(self.object_dict.get(obj.center_name).position, dtype=np.float64)) / scale
                p2 = (np.array(obj.orbit_history[len(obj.orbit_history)//2], dtype=np.float64) - np.array(self.object_dict.get(obj.center_name).orbit_history[len(self.object_dict.get(obj.center_name).orbit_history) // 2], dtype=np.float64)) / scale
                p3 = (np.array(obj.orbit_history[0], dtype=np.float64) - np.array(self.object_dict.get(obj.center_name).orbit_history[0], dtype=np.float64)) / scale

                color = QColor(150, 170, 150)
            else:
                p1 = (np.array(obj.orbit_points[0], dtype=np.float64) ) / scale
                p2 = (np.array(obj.orbit_points[1], dtype=np.float64) ) / scale
                p3 = (np.array(obj.orbit_points[2], dtype=np.float64) ) / scale
                
                color = QColor(150, 150, 170)

            if obj.obType== 'moon':
                center = np.array(self.object_dict.get('солнце').position, dtype=np.float64) / scale
            else: center = (np.array(self.object_dict.get(obj.center_name).position, dtype=np.float64) + np.array(obj.center_orbit, dtype=float)) / scale

            self.orbit_data[obj.name] = {
                'points': [p1, p2, p3],
                'center': center,
                'color': color,
                'center_name': obj.center_name,
                'object': obj.name,
                'scale': scale
            }

        self.start()

    def run(self):
        results = {}
        
        for name, data in self.orbit_data.items():
            equation = self._calculate_ellipse_equation(
                data['points'], 
                data['center'],
                data['object']
            )
            
            if equation:
                segments = self._generate_ellipse_points(equation)
                results[name] = {
                    'points': segments,
                    'color': data['color'],
                    'center': data['center'],
                    'center_name': data['center_name'],
                    'object': data['object'],
                    'scale': data['scale']
                }

        self.task_completed.emit(results)

    def _calculate_ellipse_equation(self, points, center, obj):
        try:

            p1, p2, p3 = [point - center for point in points]

            
            #print("точки элипса: ", points)
            #print("центр", center)
            #print(obj)

            M = np.array([
                [p1[0]**2, p1[0]*p1[1], p1[1]**2],
                [p2[0]**2, p2[0]*p2[1], p2[1]**2],
                [p3[0]**2, p3[0]*p3[1], p3[1]**2]
            ])

            
            v = np.array([1.0, 1.0, 1.0])
            
            A, B, C = np.linalg.solve(M, v)

            #print(f"{A}, {B}, {C}")

            if B**2 - 4*A*C >= 0:
                print("Точки не образуют эллипс")
                return None

            return {'A': A, 'B': B, 'C': C}
            
        except np.linalg.LinAlgError:
            print("np.linalg.LinAlgError")
            return None

    def _generate_ellipse_points(self, equation, num_points=100):
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
            px = r * x
            py = r * y
            points.append((px, py))
            
        return points

def angle_between_vectors(a, b):
        dot_prod = np.dot(a, b)
        norm_new_vec = np.linalg.norm(a)
        norm_last_vec = np.linalg.norm(b)

        cos_alfa = dot_prod / (norm_last_vec * norm_new_vec)
        return np.degrees(np.arccos(cos_alfa))