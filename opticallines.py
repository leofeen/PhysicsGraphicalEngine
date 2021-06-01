from plane2d import Line, Point
from math import tan, atan, degrees, radians


class ReflectionLine(Line):
    def __init__(self, sample_coordinates:Point, reflection_coefficient, angle=None, angle_coefficient=None):
        super().__init__(sample_coordinates, angle=angle, angle_coefficient=angle_coefficient)
        self.reflection_coefficient = reflection_coefficient

class RefractorLine(Line):
    def __init__(self, sample_coordinate:Point, left_coefficient, right_coefficient, angle=None, angle_coefficient=None):
        super().__init__(sample_coordinate, angle, angle_coefficient)
        self.left_coefficient = left_coefficient
        self.right_coefficient = right_coefficient

    @staticmethod
    def get_direction(refractor_line, light_beam):
        line_angle = refractor_line.angle
        if light_beam.angle == line_angle:
            return 'p' #parallel to a border
        if line_angle >= 0:
            if (light_beam.angle > -180 + line_angle) and (light_beam.angle < line_angle):
                return 'ltr' #left-to-right
        else:
            if (light_beam.angle > line_angle) and (light_beam.angle < 180 + line_angle):
                return 'ltr' #left-to-right
        return 'rtl' #right-to-left