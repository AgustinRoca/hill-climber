import math
import random

class Hiker:
    def __init__(self, name, function) -> None:
        self.name = name
        self.x = 0
        self.y = 0
        self.z = 0
        self.dx = 0
        self.dy = 0
        self.summit = False
        self._next_direction_f = function
        self.current_direction = 0
        self.random_point = None

    def set_position(self, x, y, z, dx, dy, summit):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.summit = summit

    def next_direction(self):
        # Esto en realidad se hace con herencia pero los alumnos no saben herencia
        return self._next_direction_f(self)
    
def local_max(hiker: Hiker) -> float:
    if hiker.dx == 0:
        return 0
    return math.atan2(hiker.dy, hiker.dx)

def random_walk(hiker: Hiker) -> float:
    return random.uniform(-math.pi, math.pi)

def towards_random_point(hiker: Hiker) -> float:
    if hiker.random_point:
        distance_from_random_point = math.sqrt((hiker.random_point[0] - hiker.x)**2 + (hiker.random_point[1] - hiker.y)**2)
        if distance_from_random_point < 50:
            hiker.random_point = (random.uniform(-16000, 16000), random.uniform(-16000, 16000))
    else:
        hiker.random_point = (random.uniform(-16000, 16000), random.uniform(-16000, 16000))
    return math.atan2(hiker.random_point[1] - hiker.y, hiker.random_point[0] - hiker.x)

def random_circles(hiker: Hiker) -> float:
    if hiker.current_direction == 0:
        hiker.current_direction = random.uniform(-math.pi, math.pi)
    else:
        hiker.current_direction += random.normalvariate(math.pi/500, math.pi/500)
    return hiker.current_direction
