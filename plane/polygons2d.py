from math import acos, degrees, radians, cos, sin, tan

from plane.plane2d import Polygon, Point, Vector2d

# TODO: implement arcs


class Triangle(Polygon):
    def __init__(self, first_point: Point, second_point: Point, third_point: Point) -> None:
        if first_point == second_point or second_point == third_point or first_point == third_point:
            raise ValueError(f"{first_point}, {second_point} and {third_point} are not valid vertexes for a triangle")
        super().__init__([first_point, second_point, third_point])
        a, b, c = self.edges
        # Checking triangle inequality
        if (a.length() > b.length() + c.length() or b.length() > a.length() + c.length() or c.length() > a.length() + b.length()):
            raise ValueError(f"{a.length()}, {b.length()} and {c.length()} are not valid lengths for triangle's sides")

    @staticmethod
    def construct_by_two_sides(origin: Point, first_side_length: float, second_side_length: float,
                               angle_between_sides: float, angle_from_ox: float = 0) -> 'Triangle':
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_from_ox + angle_between_sides)
        return Triangle(origin, second_point, third_point)

    @staticmethod
    def construct_by_three_sides(origin: Point, first_side_length: float, second_side_length: float,
                               third_side_length: float, angle_from_ox: float = 0) -> 'Triangle':
        angle_between_sides = degrees(acos(- (third_side_length*third_side_length - first_side_length*first_side_length 
                                           - second_side_length*second_side_length) / 2*first_side_length*second_side_length))
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_from_ox + angle_between_sides)
        return Triangle(origin, second_point, third_point)

    @staticmethod
    def construct_by_two_angles(origin: Point, first_side_length: float, angle_to_second_side: float,
                               angle_to_third_side: float, angle_from_ox: float = 0) -> 'Triangle':
        third_angle = 180 - angle_to_second_side - angle_to_third_side
        second_side_length = first_side_length * ((cos(radians(angle_to_second_side)
                                + cos(radians(angle_to_second_side)*cos(radians(third_angle)))))
                                / (sin(radians(third_angle))*sin(radians(third_angle))))
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_to_second_side + angle_from_ox)
        return Triangle(origin, second_point, third_point)


class EquilateralTriangle(Triangle):
    def __init__(self, origin: Point,  side_length: float, angle_from_ox: float = 0) -> None:
        second_vertex = origin + Vector2d.construct_from_length(side_length, angle_from_ox)
        third_vertex = origin + Vector2d.construct_from_length(side_length, angle_from_ox + 60)
        super().__init__(origin, second_vertex, third_vertex)

    # Remove parent static constructors
    @staticmethod
    def construct_by_two_sides():
        raise NotImplementedError()

    @staticmethod
    def construct_by_three_sides():
        raise NotImplementedError()

    @staticmethod
    def construct_by_two_angles():
        raise NotImplementedError()


class RightTriangle(Triangle):
    def __init__(self, origin: Point, first_leg: float, second_leg: float, angle_from_ox: float = 0) -> None:
        second_vertex = origin + Vector2d.construct_from_length(first_leg, angle_from_ox)
        third_vertex = origin + Vector2d.construct_from_length(second_leg, angle_from_ox + 90)
        super().__init__(origin, second_vertex, third_vertex)

    @staticmethod
    def from_leg_and_angle(origin: Point, leg_length: float, angle: float,
                           angle_from_ox: float = 0, is_angle_adjasent: bool = True) -> 'RightTriangle':
        while not (-180 < angle <= 180):
            if angle > 180:
                angle += 360
            else:
                angle -= 360
        if not (0 < angle < 90):
            raise ValueError(f"Right triangle can't have {angle} degrees angle (mod 360)")
        if is_angle_adjasent:
            second_leg = leg_length * tan(radians(angle))
        else:
            second_leg = leg_length / tan(radians(angle))
        return RightTriangle(origin, leg_length, second_leg, angle_from_ox)

    @staticmethod
    def from_hypotenuse_and_angle(origin: Point, hypotenuse_length: float, angle: float,
                                  angle_from_ox: float = 0) -> 'RightTriangle':
        while not (-180 < angle <= 180):
            if angle > 180:
                angle += 360
            else:
                angle -= 360
        if not (0 < angle < 90):
            raise ValueError(f"Right triangle can't have {angle} degrees angle (mod 360)")
        adjacent_leg = hypotenuse_length * cos(radians(angle))
        non_adjesent_leg = hypotenuse_length * sin(radians(angle))
        return RightTriangle(origin, adjacent_leg, non_adjesent_leg, angle_from_ox)

    # Remove parent static constructors
    @staticmethod
    def construct_by_two_sides():
        raise NotImplementedError()

    @staticmethod
    def construct_by_three_sides():
        raise NotImplementedError()

    @staticmethod
    def construct_by_two_angles():
        raise NotImplementedError() 


class Parallelogram(Polygon):
    def __init__(self, origin: Point, first_side_length: float, second_side_length: float,
                 angle_between_sides: float, angle_from_ox: float = 0) -> None:
        first_side_vector = Vector2d.construct_from_length(first_side_length, angle_from_ox)
        second_side_vector = Vector2d.construct_from_length(second_side_length, angle_from_ox + angle_between_sides)
        second_vertex = origin + first_side_vector
        fourth_vertex = origin + second_side_vector
        third_vertex = origin + first_side_vector + second_side_vector
        super().__init__([origin, second_vertex, third_vertex, fourth_vertex])


class Rectangular(Parallelogram):
    def __init__(self, origin: Point, width: float, height: float, angle_from_ox: float = 0) -> None:
        super().__init__(origin, width, height, 90, angle_from_ox)


class Square(Rectangular):
    def __init__(self, origin: Point, side_length: float, angle_from_ox: float = 0) -> None:
        super().__init__(origin, side_length, side_length, angle_from_ox=angle_from_ox)


class Rhombus(Parallelogram):
    def __init__(self, origin: Point, side_length: float, angle_between_sides: float, angle_from_ox: float = 0) -> None:
        super().__init__(origin, side_length, side_length, angle_between_sides, angle_from_ox)