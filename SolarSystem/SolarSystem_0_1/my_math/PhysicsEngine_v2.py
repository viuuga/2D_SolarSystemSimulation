import numpy as np
from typing import List
from space_objects.physicalObject import GravitationInfluationObject

_temp_r_vecs = np.empty((20, 3))
_temp_distances_sq = np.empty(20)

G = 6.67418478787878e-11
class PhysicsEngine2:

    @staticmethod
    def calculate_gravity(position: np.ndarray, mass: float, 
                         gravitation_influences: List[GravitationInfluationObject]) -> np.ndarray:
        if not gravitation_influences:
            return np.zeros(3)
    
        other_positions = np.array([obj.position for obj in gravitation_influences])
        other_masses = np.array([obj.mass for obj in gravitation_influences])

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
    def update_position(data: dict) -> dict:
        position = np.array(data['position'], dtype=float)
        velocity = np.array(data['velocity'], dtype=float)
        acceleration = np.array(data['acceleration'], dtype=float)
        last_acceleration = np.array(data['last_acceleration'], dtype=float)
    
        if len(data['gravitation_influences']) == 0:
            position += velocity * data['delta_time']
        else:
            last_acceleration = acceleration.copy()
            acceleration = PhysicsEngine2.calculate_gravity(
                position, data['mass'], data['gravitation_influences']
            )
        
            position += velocity * data['delta_time'] + 0.5 * last_acceleration * data['delta_time']**2
            velocity += 0.5 * (last_acceleration + acceleration) * data['delta_time']
    
        return {
            'position': position.tolist(),
            'velocity': velocity.tolist(),
            'acceleration': acceleration.tolist(),
            'last_acceleration': last_acceleration.tolist(),
            'mass': data['mass'],
            'gravitation_influences': data['gravitation_influences'],
            'delta_time': data['delta_time'],
            'name': data['name']
        }