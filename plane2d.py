from typing import Any, Literal, Union
from math import radians, degrees, sqrt, tan, atan, fabs, cos, sin, inf

import numpy as np


# same (collision); left-or-up; right-or-up; right-or-down; left-or-down; outside; inside
DirectionType = Literal['s', 'lou', 'rou', 'rod', 'lod', 'out', 'in']


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}; {self.y})'

    def __eq__(self, other: Union[Any, 'Point', 'Vector2d']) -> bool:
        if not isinstance(other, Point) and not isinstance(other, Vector2d):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __add__(self, other: 'Vector2d') -> 'Point':
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2d') -> 'Point':
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def as_vector(self) -> 'Vector2d':
        return Vector2d(self.x, self.y)

    def get_distance_to_point(self, point: 'Point') -> float:
        return sqrt((self.x - point.x)**2 + (self.y - point.y)**2)


#TODO: support Vector2d instead of Point where needed
class Vector2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Vector2d({self.x}, {self.y})'

    def __eq__(self, other: Union[Any, 'Point', 'Vector2d']) -> bool:
        if not isinstance(other, Point) and not isinstance(other, Vector2d):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self) -> str:
        return f'({self.x}; {self.y})'

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __add__(self, other: Union['Vector2d', Point]) -> 'Vector2d':
        if not isinstance(other, Point) or not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Union['Vector2d', Point]) -> 'Vector2d':
        if not isinstance(other, Point) or not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float, 'Vector2d']) -> Union['Vector2d', float]:
        """Returns dot product if Vector2d is passed"""
        if isinstance(scalar, Vector2d):
            return self.x * scalar.x + self.y * scalar.y
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            return NotImplemented
        return Vector2d(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: Union[int, float]) -> 'Vector2d':
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            return NotImplemented
        return Vector2d(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: Union[int, float]) -> 'Vector2d':
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            return NotImplemented
        return Vector2d(self.x // scalar, self.y // scalar)

    def __matmul__(self, other: 'Vector2d') -> float:
        if not isinstance(other, Vector2d):
            return NotImplemented
        return self.x*other.y - self.y*other.x

    def as_point(self) -> Point:
        return Point(self.x, self.y)
    
    def length(self) -> float:
        return sqrt(self.x*self.x + self.y*self.y)

    @staticmethod
    def construct_from_length(length: float, angle: float = 0) -> 'Vector2d':
        x = length * cos(radians(angle))
        y = length * sin(radians(angle))
        return Vector2d(x, y)

    @staticmethod
    def construct_from_two_points(start_point: Point, end_point: Point) -> 'Vector2d':
        return Vector2d(end_point.x - start_point.x, end_point.y - start_point.y)


class Line:
    def __init__(self, sample_coordinates: Union[Point, Vector2d],
                 angle: float = None, angle_coefficient: float = None) -> None:
        """
        Constructs a line, that goes through given point.
        Angle must be in degrees.
        """
        if angle is None and angle_coefficient is None:
            raise ValueError('Neither angle or coefficient was not given')
        if angle_coefficient is None:
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
                self.angle_coefficient = inf
                self.angle = 90
        else:
            self.angle_coefficient = angle_coefficient
            if self.angle_coefficient != inf:
                self.angle = degrees(atan(angle_coefficient))
            else:
                self.angle = 90
        if isinstance(sample_coordinates, Point):
            self.sample_coordinates = sample_coordinates
        elif isinstance(sample_coordinates, Vector2d):
            self.sample_coordinates = self.as_point()
        if self.angle_coefficient != inf:
            self.oy_segment = sample_coordinates.y - self.angle_coefficient*sample_coordinates.x
        else:
            self.oy_segment = None

    def get_y_coordinate(self, x: float) -> Union[float, None]:
        """
        Returns y coordinate for point on line with given x.
        If line parallel to Oy and given x doesn't equals to x of line,
        than None will be returned.
        """
        if self.angle_coefficient != inf:
            return self.angle_coefficient*x + self.oy_segment
        else:
            return x if x == self.sample_coordinates.x else None

    def get_direction_to_point(self, point: Union[Point, Vector2d]) -> DirectionType:
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

    def get_distance_to_point(self, point: Point) -> float:
        if self.angle_coefficient != inf:
            return fabs(self.angle_coefficient*point.x - point.y + self.oy_segment) / sqrt(self.angle_coefficient**2 + 1)
        return fabs(point.x - self.sample_coordinates.x)

    def get_intersection_point(self, line: Union['Line', 'LineSegment']) -> Union[Point, None]:
        return Line.get_intersection_point(line, self)

    def __repr__(self) -> str:
        return f'Line({self.sample_coordinates}, {self.angle})'

    @staticmethod
    def angle_between(first_line: Union['Line', 'LineSegment'], second_line: Union['Line', 'LineSegment']) -> float:
        if isinstance(first_line, Line):
            a1 = first_line.angle
        elif isinstance(first_line, LineSegment):
            a1 = first_line.reconstruct_line().angle

        if isinstance(second_line, Line):
            a2 = second_line.angle
        elif isinstance(second_line, LineSegment):
            a2 = second_line.reconstruct_line().angle

        if a1 == a2:
            return 0
        if (a1 > 0 and a2 > 0) or (a1 < 0 and a2 < 0):
            angle = fabs(a1 - a2)
        else:    
            angle = fabs(a1) + fabs(a2)
        return angle if angle <= 90 else 180 - angle
        
    @staticmethod
    def perpendicular_line(line: Union['Line', 'LineSegment'], point_from: Point = None) -> 'Line':
        if point_from is None:
            coordinates = line.sample_coordinates
        else:
            coordinates = point_from
        
        if isinstance(line, LineSegment):
            line = line.reconstruct_line()

        if line.angle_coefficient != 0:
            k = -1 / line.angle_coefficient
            return Line(coordinates, angle_coefficient=k)
        return Line(coordinates, 90)

    @staticmethod
    def get_intersection_point(first_line: Union['Line', 'LineSegment'],
                               second_line: Union['Line', 'LineSegment']) -> Union[Point, None]:
        if isinstance(first_line, LineSegment):
            first_line = first_line.reconstruct_line()
        if isinstance(second_line, LineSegment):
            second_line = second_line.reconstruct_line()
        if first_line.angle_coefficient == second_line.angle_coefficient:
            return None
        if first_line.oy_segment is not None and second_line.oy_segment is not None:
            x = (second_line.oy_segment - first_line.oy_segment) / (first_line.angle_coefficient - second_line.angle_coefficient)
            return Point(x, first_line.get_y_coordinate(x))
        if first_line.oy_segment is None:
            x = first_line.sample_coordinates.x
            return Point(x, second_line.get_y_coordinate(x))
        x = second_line.sample_coordinates.x
        return Point(x, first_line.get_y_coordinate(x))

    @staticmethod
    def construct_by_two_points(first_point: Point, second_point: Point) -> 'Line':
        if first_point.x != second_point.x:
            angle_coefficient = (second_point.y - first_point.y) / (second_point.x - first_point.x)
        else:
            angle_coefficient = inf
        return Line(first_point, angle_coefficient=angle_coefficient)

    @staticmethod
    def construct_from_vector(vector: Vector2d) -> 'Line':
        if vector.x == 0:
            angle_coefficient = inf
        else:
            angle_coefficient = vector.y / vector.x
        return Line(Point(0, 0), angle_coefficient=angle_coefficient)


class LineSegment:
    def __init__(self, first_point: Point, second_point: Point) -> None:
        self.related_line = Line.construct_by_two_points(first_point, second_point)
        if first_point.x <= second_point.x:
            self.endpoints = [first_point, second_point]
        else:
            self.endpoints = [second_point, first_point]
        self.min_x = min(first_point.x, second_point.x)
        self.max_x = max(first_point.x, second_point.x)
        self.min_y = min(first_point.y, second_point.y)
        self.max_y = max(first_point.y, second_point.y)

    def reconstruct_line(self) -> Line:
        return self.related_line

    def check_intersection(self, line: Union[Line, 'LineSegment']) -> bool:
        """Checks if intersection point lies on line segment"""
        if isinstance(line, LineSegment):
            return self.check_intersection(line.reconstruct_line()) and line.check_intersection(self.reconstruct_line())
        possible_intersection_point = Line.get_intersection_point(self.related_line, line)
        if (self.min_x <= possible_intersection_point.x <= self.max_x
            and self.min_y <= possible_intersection_point.y <= self.max_y):
            return True
        return False
    
    def get_intersection_point(self, line: Union[Line, 'LineSegment']) -> Union[Point, None]:
        """
        Warning: gives intersection point without checking
        if it is actually lies on line segment.
        Use get_intersection to ensure, that point lies on line segment.
        """
        return Line.get_intersection_point(line, self)

    def get_intersection(self, line: Union[Line, 'LineSegment']) -> tuple[bool, Union[Point, None], Line]:
        """
        Returns following tuple: (
            is point actually lies on line segment: bool,
            intersection point: Point,
            line, reconstructed from line segment: Line 
        )
        """
        if isinstance(line, Line):
            is_intersect = self.check_intersection(line)
        elif isinstance(line, LineSegment):
            is_intersect = self.check_intersection(line.reconstruct_line()) and line.check_intersection(self.reconstruct_line())
        intersection_point = self.get_intersection_point(line)
        return (is_intersect, intersection_point, self.reconstruct_line())

    def length(self) -> float:
        """Returns length of line segment"""
        return sqrt((self.endpoints[1].x - self.endpoints[0].x)**2 + (self.endpoints[1].y - self.endpoints[0].y)**2)

    def get_distance_to_point(self, point: Point) -> float:
        normal_line = Line.perpendicular_line(self.related_line, point)
        if self.check_intersection(normal_line):
            return self.related_line.get_distance_to_point(point)
        return min(point.get_distance_to_point(self.endpoints[0]), 
                    point.get_distance_to_point(self.endpoints[1]))

#TODO:
"""class Ray:
    def __init__(self, origin: Point, angle: float):
        self.related_line = Line(origin, angle)
        self.angle = angle
        while not (-180 < self.angle <= 180):
            if self.angle > 180:
                self.angle -= 360
            else:
                self.angle += 360

    def get_intersection_point(self, )"""


class Polygon:
    def __init__(self, vertexes: list[Point]) -> None:
        """
        Constructs a polygon, using vertexes in given order.
        """
        if len(vertexes) <= 2: raise ValueError(f'Expected at least 3 vertexes, but {len(vertexes)} was given')
        if len(set(vertexes)) < len(vertexes): raise ValueError(f"Polygon can't have two xertexes at the same point")

        self.vertexes = vertexes
        self.edges: list[LineSegment] = []
        for i in range(len(vertexes)):
            if i == len(vertexes) - 1:
                self.edges.append(LineSegment(vertexes[i], vertexes[0]))
            else:
                self.edges.append(LineSegment(vertexes[i], vertexes[i+1]))
        self.max_y = max([point.y for point in vertexes])
        self.min_y = min([point.y for point in vertexes])
        self.max_x = max([point.x for point in vertexes])
        self.min_x = min([point.x for point in vertexes])
        self.number_of_edges = len(self.edges)
        self.number_of_vertexes = len(vertexes)

    def is_point_inside(self, point: Point) -> bool:
        if not (self.min_y <= point.y <= self.max_y) or not (self.min_x <= point.x <= self.max_x):
            return False
        # Based on https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
        is_inside = False
        j = self.number_of_vertexes - 1
        for i in range(self.number_of_vertexes):
            if (((self.vertexes[i].y > point.y) != (self.vertexes[j].y > point.y))
                 and (point.x < (self.vertexes[j].x - self.vertexes[i].x) * (point.y - self.vertexes[i].y) 
                 / (self.vertexes[j].y - self.vertexes[i].y) + self.vertexes[i].x)):
                is_inside = not is_inside
            j = i
        return is_inside


class Cirlce:
    def __init__(self, centre: Point, radius: float) -> None:
        self.radius = radius
        self.centre = centre

    def signed_distance_to_circle_from_point(self, point: Point) -> float:
        return sqrt((self.centre.x - point.x)**2 + (self.centre.y - point.y)**2) - self.radius

    def check_intersection(self, line: Union[Line, LineSegment]) -> bool:
        distance = line.get_distance_to_point(self.centre)
        if distance > self.radius:
            return False
        if isinstance(line, Line):
            return True
        distance_first = self.centre.get_distance_to_point(line.endpoints[0])
        distance_second = self.centre.get_distance_to_point(line.endpoints[1])
        if distance_first < self.radius and distance_second < self.radius:
            return False
        return True

    def get_tangent_line(self, point_on_circumference: Point) -> Line:
        distance = self.centre.get_distance_to_point(point_on_circumference)
        if fabs(distance - self.radius) > 0.05:
            raise ValueError(f'''Point must be on circumference, but {point_on_circumference} 
                              was given with distance {distance} to a centre of circle {self}''')
        return Line.perpendicular_line(Line.construct_by_two_points(self.centre, point_on_circumference), point_on_circumference)

    def get_intersection(self, line: Union[Line, LineSegment]) -> tuple[bool, Union[Point, None], Union[Point, None]]:
        is_intersection = self.check_intersection(line)
        if not is_intersection:
            return (False, None, None)
        is_line = isinstance(line, Line)
        normal_to_line = Line.perpendicular_line(line, self.centre)
        closest_point = Line.get_intersection_point(normal_to_line, line)
        distance = self.centre.get_distance_to_point(closest_point)
        step_size_to_circumference = sqrt(self.radius*self.radius - distance*distance)
        if is_line:
            angle = line.angle
        elif not is_line:
            angle = line.reconstruct_line().angle
        first_point = closest_point + Vector2d.construct_from_length(step_size_to_circumference, angle)
        second_point = closest_point + Vector2d.construct_from_length(step_size_to_circumference, 180 + angle)
        if is_line:
            return (True, first_point, second_point)
        # Exclude points, that intersects only with related line, but don't with line segment itself
        if line.min_x > first_point.x or line.max_x < first_point.x or line.max_y < first_point.y or line.max_y > first_point.y:
            first_point = None
        if line.min_x > second_point.x or line.max_x < second_point.x or line.max_y < second_point.y or line.max_y > second_point.y:
            second_point = None
        return (True, first_point, second_point)

    def is_point_inside(self, point: Point) -> bool:
        distance = self.centre.get_distance_to_point(point)
        if distance <= self.radius:
            return True
        return False

    def get_direction_to_point(self, point: Point) -> DirectionType:
        distance = self.centre.get_distance_to_point(point)
        if distance > self.radius:
            return 'out'
        if distance == self.radius:
            return 's'
        return 'in'

    def __str__(self) -> str:
        return f'Circle({self.centre}, {self.radius})'
            
 
class Plane:
    ORIGIN = Point(0, 0)

    def __init__(self, width: int, height: int = None) -> None:
        """Pass only width to get a square plane"""
        self._plane = []
        if height is not None:
            for _ in range(height):
                self._plane.append([0]*width)
        else:
            for _ in range(width):
                self._plane.append([0]*width)
        self._plane = np.array(self._plane, int)
        self.width = width
        if height is not None:
            self.height = height
        else:
            self.height = width
        self.borders = {
            'left': Line(self.ORIGIN, 90),
            'bottom': Line(self.ORIGIN, 0),
            'top': Line(Point(self.width, self.height), 0),
            'right': Line(Point(self.width, self.height), 90),
        }
        self.objects_on_plane: list[Line, LineSegment] = []

    def size(self) -> tuple[int, int]:
        """Returns size of the plane"""
        return (self.width, self.height)

    def get_point(self, coordinates: Point) -> int:
        if coordinates.x >= self.width or coordinates.y >= self.height or coordinates.x < 0 or coordinates.y < 0:
            return None
        return self._plane[coordinates.y][coordinates.x]

    def set_point(self, coordinates: Point, value: int) -> None:
        if coordinates.x >= self.width or coordinates.y >= self.height or coordinates.x < 0 or coordinates.y < 0:
            return None
        self._plane[coordinates.y][coordinates.x] = value

    def borders_as_list(self) -> list[Line]:
        return [self.borders[key] for key in self.borders]

    def append_object(self, object_to_append: Any):
        self.objects_on_plane.append(object_to_append)

    def get_closest_object(self, point: Point) -> Any:
        closest = None
        min_distance = inf
        for obj in self.objects_on_plane:
            distance = obj.get_distance_to_point(point)
            if distance < min_distance:
                closest = obj
        return closest