from math import sin, cos, radians

from plane2d import Polygon, Point
from opticallines import LightTransparentMixin, ReflectionSegment, RefractionSegment


class ReflectionPolygon(Polygon):
    def __init__(self, vertexes: list[Point], reflection_coefficient: float):
        super().__init__(vertexes)
        self.edges: list[ReflectionSegment] = []
        for i in range(len(vertexes)):
            if i == len(vertexes) - 1:
                self.edges.append(ReflectionSegment(vertexes[i], vertexes[0], reflection_coefficient))
            else:
                self.edges.append(ReflectionSegment(vertexes[i], vertexes[i+1], reflection_coefficient))

    @staticmethod
    def from_polygon(polygon: Polygon, reflection_coefficient: float):
        return ReflectionPolygon(polygon.vertexes, reflection_coefficient)


class RefractionPolygon(Polygon, LightTransparentMixin):
    def __init__(self, vertexes: list[Point], inner_refraction_coefficient: float,
                outer_refraction_coefficient: float = 1, *, transparensy: float = 1):
        super().__init__(vertexes)
        LightTransparentMixin.__init__(self, transparensy)
        edges: list[RefractionSegment] = []
        previous_angle = self.edges[-1].reconstruct_line().angle
        for non_optical_edge in self.edges:
            current_angle = non_optical_edge.reconstruct_line().angle
            if current_angle != 0 and previous_angle != 0:
                sample_point = Point(non_optical_edge.endpoints[0].x + .1, non_optical_edge.endpoints[0].y)
            else:
                sample_point = Point(non_optical_edge.endpoints[0].x, non_optical_edge.endpoints[0].y - .1)
            if self.is_point_inside(sample_point):
                edges.append(RefractionSegment(non_optical_edge.endpoints[0], non_optical_edge.endpoints[1], inner_refraction_coefficient, outer_refraction_coefficient))
            else:
                edges.append(RefractionSegment(non_optical_edge.endpoints[0], non_optical_edge.endpoints[1], outer_refraction_coefficient, inner_refraction_coefficient))
        self.edges: list[RefractionSegment] = edges
        self.inner_refraction_coefficient = inner_refraction_coefficient
        self.outer_refraction_coefficient = outer_refraction_coefficient

    @staticmethod
    def from_polygon(polygon: Polygon, inner_refraction_coefficient: float, outer_refraction_coefficient: float = 1):
        return RefractionPolygon(polygon.vertexes, inner_refraction_coefficient, outer_refraction_coefficient)
