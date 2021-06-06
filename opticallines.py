from plane2d import Line, Point, LineSegment


class LightTransparentMixin:
    def __init__(self, transparensy: float = 1) -> None:
        if not (0 <= transparensy <= 1):
            raise ValueError(f'Transparensy must be in [0; 1], but {transparensy} was given')
        self.transparensy = transparensy


class ReflectionLine(Line):
    def __init__(self, sample_coordinates: Point, reflection_coefficient: float,
                 angle: float = None, angle_coefficient: float = None):
        super().__init__(sample_coordinates, angle=angle, angle_coefficient=angle_coefficient)
        if 0 <= reflection_coefficient <= 1:
            self.reflection_coefficient = reflection_coefficient
        else:
            raise ValueError(f'Reflection coefficient must be in [0; 1], but {reflection_coefficient} was given')

    @staticmethod
    def construct_from_line(line: Line, reflection_coefficient: float):
        return ReflectionLine(line.sample_coordinates, reflection_coefficient, line.angle)


class RefractionLine(ReflectionLine, LightTransparentMixin):
    def __init__(self, sample_coordinates: Point, left_refraction_coefficient: float, 
                right_refraction_coefficient: float, angle: float = None, angle_coefficient: float = None,
                *, transparensy: float = 1):
        super().__init__(sample_coordinates, reflection_coefficient=1, angle=angle, angle_coefficient=angle_coefficient)
        LightTransparentMixin.__init__(self, transparensy)
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

    def get_current_refraction_coefficient(self, direction: str):
        if direction == 'lou' or direction == 'lod':
            return self.left_refraction_coefficient
        elif direction == 'rou' or direction == 'rod':
            return self.right_refraction_coefficient
        raise ValueError(f'Unsopported direction: {direction}')

    @staticmethod
    def construct_from_line(line: Line, left_refraction_coefficient: float, right_refraction_coefficient: float):
        return RefractionLine(line.sample_coordinates, left_refraction_coefficient, right_refraction_coefficient, line.angle)


class ReflectionSegment(LineSegment):
    def __init__(self, first_point: Point, second_point: Point, reflection_coefficient: float):
        super().__init__(first_point, second_point)
        self.related_line = ReflectionLine.construct_from_line(self.reconstruct_line(), reflection_coefficient)


class RefractionSegment(LineSegment, LightTransparentMixin):
    def __init__(self, first_point: Point, second_point: Point, left_refraction_coefficient: float,
                right_refraction_coefficient: float, *, transparensy: float = 1):
        super().__init__(first_point, second_point)
        LightTransparentMixin.__init__(self, transparensy)
        self.related_line = RefractionLine.construct_from_line(self.reconstruct_line(), left_refraction_coefficient, right_refraction_coefficient)