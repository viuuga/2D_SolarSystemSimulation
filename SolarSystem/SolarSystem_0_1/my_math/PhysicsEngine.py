import numpy as np
from typing import List

G = 6.67418478787878e-11

class PhysicsEngine:
    @staticmethod
    def calculate_gravity(position: np.ndarray, mass: float, 
                         other_positions: List[np.ndarray], 
                         other_masses: List[float]) -> np.ndarray:
        r_vecs = np.array(other_positions) - position
        distances = np.linalg.norm(r_vecs, axis=1)
        
        mask = distances > 1e-10
        r_vecs = r_vecs[mask]
        distances = distances[mask]
        other_masses = np.array(other_masses)[mask]

        if len(distances) == 0:
            return np.zeros(3)

        force_mags = G * mass * other_masses / (distances**2)
        force_dirs = r_vecs / distances[:, np.newaxis]
        return np.sum(force_mags[:, np.newaxis] * force_dirs, axis=0) / mass

    @staticmethod
    def update_position(obj_data: dict, current_time: float, 
                       time_acceleration: float) -> dict:
        delta_time = (current_time - obj_data['last_update_time']) * time_acceleration
        
        if delta_time <= 0:
            return obj_data
            
        max_substep = 100
        n_substeps = max(1, int(delta_time / max_substep))
        substep = delta_time / n_substeps
        
        position = np.array(obj_data['position'])
        velocity = np.array(obj_data['velocity'])
        acceleration = np.array(obj_data['acceleration'])
        last_acceleration = np.array(obj_data['last_acceleration'])
        
        for _ in range(n_substeps):
            if not obj_data['gravitation_influences']:
                position += velocity * substep
                continue
                
            last_acceleration = acceleration.copy()
            acceleration = PhysicsEngine.calculate_gravity(
                position, obj_data['mass'],
                [inf['position'] for inf in obj_data['gravitation_influences']],
                [inf['mass'] for inf in obj_data['gravitation_influences']]
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