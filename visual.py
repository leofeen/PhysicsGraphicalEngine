from opticallines import ReflectionLine
from typing import Iterable
from PIL import Image, ImageDraw
from plane2d import Line, Plane, Point
from light_beam import LightBeam

class IByPointDraw:
    type_ = 0
    def __init__(self):
        IByPointDraw.type_ += 1
        self.type = IByPointDraw.type_
        self.draw_coordinates = set()

class VisualPlane:
    def __init__(self, width=None, height=None, plane:Plane=None):
        if plane == None:
            self.plane = Plane(width, height)
        else:
            self.plane = plane
        self.image_counter = 0
        self.type_to_color = {0: 0}

    def create_image(self):
        image = Image.new('RGB', self.plane.size())
        image_draw = ImageDraw.ImageDraw(image)
        width, height = self.plane.size()
        for x in range(width):
            for y in range(height-1, -1, -1):
                image_draw.point((x, y), self.type_to_color[self.plane.get_point(Point(x, height - 1 - y))])
        image.save(f'./imgs/image{self.image_counter}.png')
        self.image_counter += 1

    def bind_color_to_type(self, type_:int, color):
        if self.type_to_color.get(type_, None) == None:
            self.type_to_color[type_] = color
        else:
            raise KeyError(f'Type {type_} already binded to a color')

    def draw_object_by_point(self, obj:IByPointDraw):
        for coordinates in obj.draw_coordinates:
            self.plane.set_point(coordinates, obj.type_)

    def draw_by_coordinates(self, coordinates_iter:Iterable[Point], type_):
        for coordinates in coordinates_iter:
            self.plane.set_point(coordinates, type_)


class VisualLine(IByPointDraw):
    def __init__(self, line:Line, color:tuple, visual_plane:VisualPlane):
        super().__init__()
        self.line = line
        self.color = color
        self.type_ = VisualLine.type_
        self.visual_plane = visual_plane
        width, height = visual_plane.plane.size()
        if line.angle != 90:
            for x in range(width*100):
                round_x = round(x/100)
                round_y = round(line.get_y_coordinate(x/100))
                if 0 <= round_y < height:
                    self.draw_coordinates.add(Point(round_x, round_y))
        else:
            round_x = round(line.sample_coordinates.x)
            for y in range(height):
                self.draw_coordinates.add(Point(round_x, y))
        self.visual_plane.bind_color_to_type(self.type_, self.color)


class VisualLightBeam(IByPointDraw):
    def __init__(self, light_beam:LightBeam, visual_plane:VisualPlane, color:tuple):
        super().__init__()
        self.beam = light_beam
        self.visual_plane = visual_plane
        self.color = color
        self.type_ = VisualLightBeam.type_
        for point in self.beam.coordinates:
            x, y = point.x, point.y
            rounded_x = round(x)
            rounded_y = round(y)
            self.draw_coordinates.add(Point(rounded_x, rounded_y))
        self.visual_plane.bind_color_to_type(self.type_, self.color)

    def draw_source(self):
        source_center = Point(round(self.beam.coordinates[0].x), round(self.beam.coordinates[0].y))
        source_coordinates = set()
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
                    source_coordinates.add(Point(x, y))
        self.visual_plane.draw_by_coordinates(source_coordinates, self.type_)


if __name__ == '__main__':
    plane = VisualPlane(1000)
    plane.create_image()

    reflection_line = ReflectionLine(Point(500, 500), 1, -70)
    plane.plane.append_object(reflection_line)
    reflection_line2 = ReflectionLine(Point(750, 750), 1, 80)
    plane.plane.append_object(reflection_line2) 

    light_beam = LightBeam(Point(700, 700), -120)
    while True:
        object_hit = light_beam.propogate_until(plane.plane.borders_as_list() + plane.plane.objects_on_plane)
        if isinstance(object_hit, ReflectionLine):
            light_beam.reflect(object_hit)
        else:
            break
    
    visual_beam = VisualLightBeam(light_beam, plane, (255, 0, 0))
    visual_beam.draw_source()

    visual_line = VisualLine(reflection_line, (10, 255, 10), plane)
    visual_line2 = VisualLine(reflection_line2, (10, 255, 10), plane)

    plane.draw_object_by_point(visual_line)
    plane.draw_object_by_point(visual_line2)
    plane.draw_object_by_point(visual_beam)
    plane.create_image()