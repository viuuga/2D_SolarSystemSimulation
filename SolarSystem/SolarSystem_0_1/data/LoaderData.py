import json
from os import name
import numpy as np
from space_objects.physicalObject import PhysicalObject


class Loader():
    
    def __init__(self, path: str = None):
        self.objects = []
        self.objects_dict = {}
        if path == None:
            self.path = "SolarSystem_0_1/data/SolarSystem.json"
        else: self.path = path
        self.load_solar_system()

    def load_solar_system(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        
            sun = self.create_physical_object(data['sun'], "")
            self.objects.append(sun)
            self.objects_dict[sun.name] = sun

            
            for planet_name, planet_data in data.get('planets', {}).items():
                planet = self.create_physical_object(planet_data, sun.name)
                self.objects.append(planet)
                self.objects_dict[planet.name] = planet
                planet.gravitation_influences.append(sun)
                sun.gravitation_influences.append(planet)

                
                for moon_name, moon_data in planet_data.get('satellites', {}).items():
                    moon = self.create_moon_object(moon_data, planet)
                    self.objects.append(moon)
                    self.objects_dict[moon.name] = moon
                    moon.gravitation_influences.extend([planet, sun])
                    planet.gravitation_influences.append(moon)

        except Exception as e:
            print(f"Error loading solar system: {e}")

    def create_physical_object(self, obj_data, center_name):
        return PhysicalObject(
            x=obj_data['x'],
            y=obj_data['y'],
            z=obj_data.get('z', 0),
            velocity=np.array(obj_data['velocity']),
            mass=obj_data['mass'],
            texture_path=obj_data['texture'],
            radius=obj_data['radius'],
            name=obj_data['name'],
            center_name=center_name,
            obType=obj_data['type'],
            pregen_points=obj_data['orbit_points']            
        )

    def create_moon_object(self, moon_data, parent_planet):
        # Позиция спутника относительно планеты
        offset = np.array(moon_data['offset'])
        position = parent_planet.position + offset

        # Скорость спутника = скорость планеты + орбитальная скорость
        velocity = parent_planet.velocity + np.array(moon_data['velocity'])

        return PhysicalObject(
            x=position[0],
            y=position[1],
            z=position[2],
            velocity=velocity,
            mass=moon_data['mass'],
            texture_path=moon_data['texture'],
            radius=moon_data['radius'],
            name=moon_data['name'],
            center_name=parent_planet.name,
            obType=moon_data['type']
        )




