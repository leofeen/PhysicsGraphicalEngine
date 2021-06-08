from math import acos, degrees, radians, cos, sin

from plane2d import Polygon, Point, Vector2d


class Triangle(Polygon):
    def __init__(self, first_point: Point, second_point: Point, third_point: Point):
        if first_point == second_point or second_point == third_point or first_point == third_point:
            raise ValueError(f"{first_point}, {second_point} and {third_point} are not valid vertexes for a triangle")
        super().__init__([first_point, second_point, third_point])
        a, b, c = self.edges
        if (a.length() > b.length() + c.length() or b.length() > a.length() + c.length() or c.length() > a.length() + b.length()):
            raise ValueError(f"{a.length()}, {b.length()} and {c.length()} are not valid lengths for triangle's sides")

    @staticmethod
    def construct_by_two_sides(origin: Point, first_side_length: float, second_side_length: float,
                               angle_between_sides: float, angle_from_ox: float = 0):
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_from_ox + angle_between_sides)
        return Triangle(origin, second_point, third_point)

    @staticmethod
    def construct_by_three_sides(origin: Point, first_side_length: float, second_side_length: float,
                               third_side_length: float, angle_from_ox: float = 0):
        angle_between_sides = degrees(acos(- (third_side_length*third_side_length - first_side_length*first_side_length 
                                           - second_side_length*second_side_length) / 2*first_side_length*second_side_length))
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_from_ox + angle_between_sides)
        return Triangle(origin, second_point, third_point)

    @staticmethod
    def construct_by_two_angles(origin: Point, first_side_length: float, angle_to_second_side: float,
                               angle_to_third_side: float, angle_from_ox: float = 0):
        third_angle = 180 - angle_to_second_side - angle_to_third_side
        second_side_length = first_side_length * ((cos(radians(angle_to_second_side)
                                + cos(radians(angle_to_second_side)*cos(radians(third_angle)))))
                                / (sin(radians(third_angle))*sin(radians(third_angle))))
        second_point = origin + Vector2d.construct_from_length(first_side_length, angle_from_ox)
        third_point = origin + Vector2d.construct_from_length(second_side_length, angle_to_second_side + angle_from_ox)
        return Triangle(origin, second_point, third_point)


    #TODO: class RightTriangle(point, length, angle)


#TODO: class Rectangular, etc