from visual2d import Color, IByPointDraw, VisualPlane, VisualLine, VisualPoint
from light_beam import LightBeam
from plane2d import Point, Line
from opticallines import ReflectionLine, RefractionLine


class VisualLightBeam(IByPointDraw):
    def __init__(self, light_beam: LightBeam, visual_plane: VisualPlane, color: tuple):
        super().__init__()
        self.beam = light_beam
        self.visual_plane = visual_plane
        self.color = color
        self.original_color = color
        self.type_ = VisualLightBeam.type_
        self.visual_plane.bind_object(self)

    def draw_source(self):
        source_center = Point(round(self.beam.coordinates[0].x), round(self.beam.coordinates[0].y))
        for n in range(4):
            for i in range(-3, 4):
                x = source_center.x
                y = source_center.y
                if n == 0:
                    x += i
                elif n == 1:
                    y += i
                elif n == 2:
                    x -= i
                    y += i
                elif n == 3:
                    x += i
                    y += i
                if (x >= 0) and (x < self.visual_plane.plane.size()[0]) and (y >= 0) and (y < self.visual_plane.plane.size()[1]):
                    if self.draw_coordinates.get(Point(x, y), None) == None:
                        self.draw_coordinates[Point(x, y)] = self.color

    def update_intensity(self):
        new_intensity = self.beam.relative_intensity
        background_color = self.visual_plane.background_color
        self.color = Color.blend_colors(self.original_color, background_color, 1-new_intensity)

    def update_draw_coordinates(self):
        for point in self.beam.coordinates:
            x, y = point.x, point.y
            rounded_x = round(x)
            rounded_y = round(y)
            if self.draw_coordinates.get(Point(rounded_x, rounded_y), None) == None:
                self.draw_coordinates[Point(rounded_x, rounded_y)] = self.color

    def fully_propogate(self):
        while True:
            object_hit = self.beam.propogate_until(self.visual_plane.plane.borders_as_list() + self.visual_plane.plane.objects_on_plane)
            self.update_draw_coordinates()
            if isinstance(object_hit, RefractionLine):
                self.beam.refract(object_hit)
            elif isinstance(object_hit, ReflectionLine):
                self.beam.reflect(object_hit)
                self.update_intensity()
            else:
                break


class LightBeamSceneManager:
    def __init__(self, visual_plane: VisualPlane, *, beams: list[tuple[LightBeam, tuple, bool]], points: list[tuple[Point, tuple]]=None, lines: list[tuple[Line, tuple]]=None) -> None:
        self.visual_plane: VisualPlane = visual_plane

        self.points: list[Point] = []
        self.lines: list[Line] = []
        self.beams: list[LightBeam] = []

        self.visual_points: list[VisualPoint] = []
        self.visual_lines: list[VisualLine] = []
        self.visual_beams: list[VisualLightBeam] = []

        if points != None:
            for point, color in points:
                self.points.append(point)
                visual_point = VisualPoint(point, self.visual_plane, color)
                self.visual_points.append(visual_point)

        if lines != None:
            for line, color in lines:
                self.lines.append(line)
                visual_line = VisualLine(line, self.visual_plane, color)
                self.visual_lines.append(visual_line)
                self.visual_plane.plane.append_object(line)

        for beam, color, draw_source in beams:
            self.beams.append(beam)
            visual_beam = VisualLightBeam(beam, self.visual_plane, color)
            if draw_source:
                visual_beam.draw_source()
            self.visual_beams.append(visual_beam)
            
    def draw_picture(self):
        print('Started processing the scene')
        for visual_beam in self.visual_beams:
            visual_beam.fully_propogate()
        for visual_line in self.visual_lines:
            self.visual_plane.draw_object_by_point(visual_line)
        for visual_point in self.visual_points:
            self.visual_plane.draw_object_by_point(visual_point)
        for visual_beam in self.visual_beams:
            self.visual_plane.draw_object_by_point(visual_beam)
        self.visual_plane.create_image()
        print('Image created')