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
        self.random_point = None if function != spiral else (0, 0)
        self.prev_z = 0
        self.speed = 50
        self.walk_rad = 50

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
        self.current_direction = self._next_direction_f(self)
        return self.current_direction
    
    def will_be_out_of_bounds(self, angle):
        x, y = self.new_xy(angle)
        return x**2 + y**2 > 23000**2
    
    def new_xy(self, angle):
        x = self.x + self.speed * math.cos(angle)
        y = self.y + self.speed * math.sin(angle)
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
    elif hiker.prev_z > hiker.z or hiker.will_be_out_of_bounds(local_max(hiker)):
        hiker.random_point = hiker.new_random_point()
    else:
        return local_max(hiker)
    return math.atan2(hiker.random_point[1] - hiker.y, hiker.random_point[0] - hiker.x)

def spiral(hiker: Hiker) -> float:
    if hiker.random_point:
        distance_from_random_point = math.sqrt((hiker.random_point[0] - hiker.x)**2 + (hiker.random_point[1] - hiker.y)**2)
        if distance_from_random_point < 50:
            hiker.random_point = None
            return 0
        else:
            return math.atan2(hiker.random_point[1] - hiker.y, hiker.random_point[0] - hiker.x)
    new_dir = hiker.current_direction + 15/(hiker.walk_rad)
    new_x, new_y = hiker.new_xy(new_dir)
    hiker.walk_rad = math.sqrt(new_x**2 + new_y**2)
    return new_dir