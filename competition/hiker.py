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
        self.prev_z = 0

    def set_position(self, x, y, z, dx, dy, summit):
        self.prev_z = self.z
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.summit = summit

    def next_direction(self):
        # Esto en realidad se hace con herencia pero los alumnos no saben herencia
        return self._next_direction_f(self)
    
    def will_be_out_of_bounds(self, angle, speed):
        x, y = self.new_xy(angle, speed)
        return x**2 + y**2 > 23000**2
    
    def new_xy(self, angle, speed):
        x = self.x + speed * math.cos(angle)
        y = self.y + speed * math.sin(angle)
        return x, y
    
    def new_random_point(self):
        circle_r = 23000
        alpha = 2 * math.pi * random.random()
        r = circle_r * math.sqrt(random.random())
        x = r * math.cos(alpha)
        y = r * math.sin(alpha)
        return x, y
    
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
            hiker.random_point = hiker.new_random_point()
    else:
        hiker.random_point = hiker.new_random_point()
    return math.atan2(hiker.random_point[1] - hiker.y, hiker.random_point[0] - hiker.x)

def random_circles(hiker: Hiker) -> float:
    if hiker.current_direction == 0:
        hiker.current_direction = random.uniform(-math.pi, math.pi)
    else:
        hiker.current_direction += random.normalvariate(math.pi/500, math.pi/500)
    return hiker.current_direction

def local_max_with_reset(hiker: Hiker) -> float:
    if hiker.random_point:
        distance_from_random_point = math.sqrt((hiker.random_point[0] - hiker.x)**2 + (hiker.random_point[1] - hiker.y)**2)
        if distance_from_random_point < 50:
            hiker.random_point = hiker.new_random_point()
        else:
            hiker.random_point = None
            return local_max(hiker)
    elif hiker.prev_z > hiker.z:
        hiker.random_point = hiker.new_random_point()
    else:
        return local_max(hiker)
    return math.atan2(hiker.random_point[1] - hiker.y, hiker.random_point[0] - hiker.x)