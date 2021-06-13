from plane2d import Cirlce, Polygon, Point
from opticallines import LightTransparentMixin, ReflectionLine, ReflectionSegment, RefractionLine, RefractionSegment


class ReflectionPolygon(Polygon):
    def __init__(self, vertexes: list[Point], reflection_coefficient: float) -> None:
        super().__init__(vertexes)
        self.edges: list[ReflectionSegment] = []
        for i in range(len(vertexes)):
            if i == len(vertexes) - 1:
                self.edges.append(ReflectionSegment(vertexes[i], vertexes[0], reflection_coefficient))
            else:
                self.edges.append(ReflectionSegment(vertexes[i], vertexes[i+1], reflection_coefficient))

    @staticmethod
    def from_polygon(polygon: Polygon, reflection_coefficient: float) -> 'ReflectionPolygon':
        return ReflectionPolygon(polygon.vertexes, reflection_coefficient)


class RefractionPolygon(Polygon, LightTransparentMixin):
    def __init__(self, vertexes: list[Point], inner_refraction_coefficient: float,
                outer_refraction_coefficient: float = 1, *, transparensy: float = 1) -> None:
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
                edges.append(RefractionSegment(non_optical_edge.endpoints[0], non_optical_edge.endpoints[1],
                                               inner_refraction_coefficient, outer_refraction_coefficient))
            else:
                edges.append(RefractionSegment(non_optical_edge.endpoints[0], non_optical_edge.endpoints[1],
                                               outer_refraction_coefficient, inner_refraction_coefficient))
        self.edges: list[RefractionSegment] = edges
        self.inner_refraction_coefficient = inner_refraction_coefficient
        self.outer_refraction_coefficient = outer_refraction_coefficient

    @staticmethod
    def from_polygon(polygon: Polygon, inner_refraction_coefficient: float,
                     outer_refraction_coefficient: float = 1) -> 'RefractionPolygon':
        return RefractionPolygon(polygon.vertexes, inner_refraction_coefficient, outer_refraction_coefficient)


class ReflectionCircle(Cirlce):
    def __init__(self, centre: Point, radius: float, reflection_coefficient: float = 1) -> None:
        super().__init__(centre, radius)
        self.reflection_coefficient = reflection_coefficient

    def get_tangent_line(self, point_on_circumference: Point) -> ReflectionLine:
        tangent_line = super().get_tangent_line(point_on_circumference)
        return ReflectionLine.construct_from_line(tangent_line, self.reflection_coefficient)


class RefractionCircle(Cirlce):
    def __init__(self, centre: Point, radius: float,
                 inner_refraction_coefficient: float, outer_refraction_coefficient: float = 1) -> None:
        super().__init__(centre, radius)
        self.inner_refraction_coefficient = inner_refraction_coefficient
        self.outer_refraction_coefficient = outer_refraction_coefficient


    def get_tangent_line(self, point_on_circumference: Point) -> RefractionLine:
        tangent_line = super().get_tangent_line(point_on_circumference)
        direction = tangent_line.get_direction_to_point(self.centre)
        if direction == 'lod' or direction == 'lou':
            return RefractionLine.construct_from_line(tangent_line, self.inner_refraction_coefficient, self.outer_refraction_coefficient)
        return RefractionLine.construct_from_line(tangent_line, self.outer_refraction_coefficient, self.inner_refraction_coefficient)