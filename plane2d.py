import math
import numpy as np
from math import radians, degrees, tan, atan, fabs


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}; {self.y})'


class Line:
    def __init__(self, sample_coordinates:Point, angle=None, angle_coefficient=None):
        """Angle in degrees"""
        if angle == None and angle_coefficient == None:
            raise ValueError('Neither angle or coefficient was not given')
        if angle_coefficient == None:
            self.angle = angle
            while self.angle < -180 or self.angle > 180:
                if self.angle < -180:
                    self.angle += 360
                else:
                    self.angle -= 360
            if self.angle != 90 and self.angle != -90:
                self.angle_coefficient = tan(radians(angle))
                self.angle = degrees(atan(self.angle_coefficient))
            else:
                self.angle_coefficient = math.inf
                self.angle = 90
        else:
            self.angle_coefficient = angle_coefficient
            self.angle = degrees(atan(angle_coefficient))
        self.sample_coordinates = sample_coordinates
        if self.angle_coefficient != math.inf:
            self.oy_segment = sample_coordinates.y - self.angle_coefficient*sample_coordinates.x
        else:
            self.oy_segment = None

    def get_y_coordinate(self, x):
        if self.angle_coefficient != math.inf:
            return self.angle_coefficient*x + self.oy_segment
        else:
            return x if x == self.sample_coordinates.x else None

    def get_direction_to_point(self, point:Point):
        if self.angle == 90:
            if point.x == self.sample_coordinates.x:
                return 's'
            if point.x < self.sample_coordinates.x:
                return 'lou'
            return 'rod'
        line_y = self.get_y_coordinate(point.x)
        if line_y == point.y:
            return 's'
        if line_y < point.y and self.angle >= 0:
            return 'lou' #left-or-up
        elif line_y > point.y and self.angle >= 0:
            return 'rod' #right-or-down
        elif line_y < point.y:
            return 'rou' #right-or-up
        return 'lod' #left-or-down

    @staticmethod
    def angle_between(first_line, second_line):
        a1 = first_line.angle
        a2 = second_line.angle
        if a1 == a2:
            return 0
        if (a1 > 0 and a2 > 0) or (a1 < 0 and a2 > 0):
            angle = fabs(a1 - a2)
        else:    
            angle = fabs(a1) + fabs(a2)
        return angle if angle <= 90 else 180 - angle
        
    @staticmethod
    def perpendicular_line(line, point_from=None):
        if point_from == None:
            coordinates = line.sample_coordinates
        else:
            coordinates = point_from
        if line.angle_coefficient != 0:
            k = -1 / line.angle_coefficient
            return Line(coordinates, angle_coefficient=k)
        return Line(coordinates, 90)

    @staticmethod
    def get_intersection_point(first_line, second_line):
        if first_line.angle_coefficient == second_line.angle_coefficient:
            return None
        if first_line.oy_segment != None and second_line.oy_segment != None:
            x = (second_line.oy_segment - first_line.oy_segment) / (first_line.angle_coefficient - second_line.angle_coefficient)
            return Point(x, first_line.get_y_coordinate(x))
        if first_line.oy_segment == None:
            x = first_line.sample_coordinates.x
            return Point(x, second_line.get_y_coordinate(x))
        x = second_line.sample_coordinates.x
        return Point(x, first_line.get_y_coordinate(x))
            


class Plane:
    ORIGIN = Point(0, 0)

    def __init__(self, width, height=None):
        """Pass only width to get a square"""
        self._plane = []
        if height != None:
            for _ in range(height):
                self._plane.append([0]*width)
        else:
            for _ in range(width):
                self._plane.append([0]*width)
        self._plane = np.array(self._plane, int)
        self.width = width
        if height != None:
            self.height = height
        else:
            self.height = width
        self.borders = {
            'left': Line(self.ORIGIN, 90),
            'bottom': Line(self.ORIGIN, 0),
            'top': Line(Point(self.width, self.height), 0),
            'right': Line(Point(self.width, self.height), 90),
        }
        self.objects_on_plane = []

    def size(self):
        return (self.width, self.height)

    def get_point(self, coordinates:Point):
        if coordinates.x >= self.width or coordinates.y >= self.height or coordinates.x < 0 or coordinates.y < 0:
            return None
        return self._plane[coordinates.y][coordinates.x]

    def set_point(self, coordinates:Point, value:int):
        if coordinates.x >= self.width or coordinates.y >= self.height or coordinates.x < 0 or coordinates.y < 0:
            return None
        self._plane[coordinates.y][coordinates.x] = value

    def borders_as_list(self):
        return [self.borders[key] for key in self.borders]

    def append_object(self, object_to_append):
        self.objects_on_plane.append(object_to_append)