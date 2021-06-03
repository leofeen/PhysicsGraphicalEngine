from plane2d import Line, Point
from math import tan, atan, degrees, radians


class ReflectionLine(Line):
    def __init__(self, sample_coordinates:Point, reflection_coefficient: float, angle: float=None, angle_coefficient: float=None):
        super().__init__(sample_coordinates, angle=angle, angle_coefficient=angle_coefficient)
        if 0 <= reflection_coefficient <= 1:
            self.reflection_coefficient = reflection_coefficient
        else:
            raise ValueError(f'Reflection coefficient must be in [0; 1], but {reflection_coefficient} was given')


class RefractionLine(ReflectionLine):
    def __init__(self, sample_coordinates: Point, left_refraction_coefficient: float, 
                right_refraction_coefficient: float, angle: float=None, angle_coefficient: float=None):
        super().__init__(sample_coordinates, reflection_coefficient=1, angle=angle, angle_coefficient=angle_coefficient)
        if left_refraction_coefficient < 1 or right_refraction_coefficient < 1:
            raise ValueError(f'Refraction coefficients must be greater or equal to 1, \
                                but {left_refraction_coefficient} and {right_refraction_coefficient} was given')
        self.left_refraction_coefficient = left_refraction_coefficient #top coefficient for horizontal line
        self.right_refraction_coefficient = right_refraction_coefficient #bottom coefficient for horizontal line

    def get_new_refraction_coefficient(self, direction: str):
        if direction == 'lou' or direction == 'lod':
            return self.right_refraction_coefficient
        elif direction == 'rou' or direction == 'rod':
            return self.left_refraction_coefficient
        raise ValueError(f'Unsopported direction: {direction}')