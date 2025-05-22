import numpy as np
from typing import List

_temp_r_vecs = np.empty((20, 3))  # Предполагаем максимум 100 объектов
_temp_distances_sq = np.empty(20)

G = 6.67418478787878e-11
class PhysicsEngine:
    @staticmethod
    def calculate_gravity(position: np.ndarray, mass: float, 
                         other_positions: List[np.ndarray], 
                         other_masses: List[float]) -> np.ndarray:
        # Преобразуем входные данные в массивы NumPy
        other_positions = np.array(other_positions)
        other_masses = np.array(other_masses)
    
        r_vecs = other_positions - position
        distances = np.linalg.norm(r_vecs, axis=1)
    
        mask = distances > 1e-10
        r_vecs = r_vecs[mask]
        distances = distances[mask]
        other_masses = other_masses[mask]

        if len(distances) == 0:
            return np.zeros(3)

        force_mags = G * mass * other_masses / (distances**2)
        force_dirs = r_vecs / distances[:, np.newaxis]
        return np.sum(force_mags[:, np.newaxis] * force_dirs, axis=0) / mass

    @staticmethod
    def update_position(obj_data: dict, current_time: float, time_acceleration: float) -> dict:
        delta_time = (current_time - obj_data['last_update_time']) * time_acceleration
    
        if delta_time <= 0:
            return obj_data
        
        # Преобразуем гравитационные влияния в массивы NumPy один раз
        influences = obj_data['gravitation_influences']
        if influences:
            other_positions = np.array([inf['position'] for inf in influences])
            other_masses = np.array([inf['mass'] for inf in influences])
        else:
            other_positions = np.empty((0, 3))
            other_masses = np.empty(0)
    
        max_substep = 100
        n_substeps = max(1, int(delta_time / max_substep))
        substep = delta_time / n_substeps
    
        position = np.array(obj_data['position'])
        velocity = np.array(obj_data['velocity'])
        acceleration = np.array(obj_data['acceleration'])
        last_acceleration = np.array(obj_data['last_acceleration'])
    
        for _ in range(n_substeps):
            if len(other_masses) == 0:
                position += velocity * substep
                continue
            
            last_acceleration = acceleration.copy()
            acceleration = PhysicsEngine.calculate_gravity(
                position, obj_data['mass'], other_positions, other_masses
            )
        
            position += velocity * substep + 0.5 * last_acceleration * substep**2
            velocity += 0.5 * (last_acceleration + acceleration) * substep
    
        return {
            'position': position.tolist(),
            'velocity': velocity.tolist(),
            'acceleration': acceleration.tolist(),
            'last_acceleration': last_acceleration.tolist(),
            'last_update_time': current_time,
            'mass': obj_data['mass'],
            'gravitation_influences': obj_data['gravitation_influences']
        }