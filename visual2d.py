from opticallines import LightTransparentMixin
from typing import Any, Iterable, Union
from PIL import Image, ImageDraw
from plane2d import Line, LineSegment, Plane, Point, Polygon


class Color:
    #NONE color used for invinsible objects
    NONE = (None, None, None) 
    #TODO: add more colors
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 0, 90)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    LIGHT_GREEN = (0, 255, 90)
    BLACK = (0, 0, 0)
    AQUA = (0, 255, 255)

    @staticmethod
    def blend_colors(first_color: tuple[int], second_color: tuple[int], blending_coefficient: float):
        if not (0 <= blending_coefficient <= 1):
            raise ValueError(f'Blending coefficient must be in [0; 1], but {blending_coefficient} was given')

        new_red = pow((1 - blending_coefficient)*(first_color[0]**2) + blending_coefficient*(second_color[0]**2), 1/2)
        new_green = pow((1 - blending_coefficient)*(first_color[1]**2) + blending_coefficient*(second_color[1]**2), 1/2)
        new_blue = pow((1 - blending_coefficient)*(first_color[2]**2) + blending_coefficient*(second_color[2]**2), 1/2)
        return (round(new_red), round(new_green), round(new_blue))


#Every class, that wraps object to be drawed on scene, should inheret form IByPointDraw, providing
#realization for filling self.draw_coordinates dict in form of 'Point(x, y): color,'
#and storing IByPointDraw.type_ in self.type_
class IByPointDraw:
    type_ = 0
    def __init__(self, obj: Any):
        IByPointDraw.type_ += 1
        self.type = IByPointDraw.type_
        self.draw_coordinates: dict[Point, tuple] = {}
        self.color = (0, 0, 0)
        self.transparensy = 1
        if isinstance(obj, LightTransparentMixin):
            self.transparensy = obj.transparensy

    def get_color_on_point(self, coordinates: tuple):
        return self.draw_coordinates.get(Point(coordinates[0], coordinates[1]), self.color)


class VisualPlane:
    def __init__(self, width: int = None, height: int = None, *, plane: Plane = None,
                 path_to_image_folder: str = '', background_color: tuple[int] = Color.BLACK):
        if plane == None:
            self.plane = Plane(width, height)
        else:
            self.plane = plane
        self.image_counter = 0
        self.type_to_object: dict[int, Union[VisualPlane, IByPointDraw]] = {0: self}
        if path_to_image_folder == '':
            self.path_to_image_folder = '.'
        else:
            self.path_to_image_folder = path_to_image_folder
        self.background_color = background_color

    def create_image(self, image_name: str = ''):
        image = Image.new('RGB', self.plane.size())
        image_draw = ImageDraw.ImageDraw(image)
        width, height = self.plane.size()
        for x in range(width):
            for y in range(height-1, -1, -1):
                image_draw.point((x, y), self.type_to_object[self.plane.get_point(Point(x, height - 1 - y))].get_color_on_point((x, height - 1 - y)))
        if image_name == '':
            image.save(f'{self.path_to_image_folder}/image{self.image_counter}.png')
        else:
            image.save(f'{self.path_to_image_folder}/{image_name}.png')
        self.image_counter += 1

    def bind_object(self, obj: IByPointDraw):
        if self.type_to_object.get(obj.type_, None) == None:
            self.type_to_object[obj.type_] = obj
        else:
            raise KeyError(f'Type {obj.type_} already binded to a color')

    def draw_object_by_point(self, obj: IByPointDraw):
        for coordinates in obj.draw_coordinates:
            self.plane.set_point(coordinates, obj.type_)

    def draw_by_coordinates(self, coordinates_iter: Iterable[Point], type_: int):
        for coordinates in coordinates_iter:
            self.plane.set_point(coordinates, type_)

    def get_color_on_point(self, point: Point):
        return self.background_color

    def reset_plane(self):
        self.type_to_object = {0: self}
        width, height = self.plane.size()
        self.plane = Plane(width, height)

    def get_value_on_point(self, point: Point):
        return self.plane.get_point(point)

    def get_binded_object(self, type_: int):
        return self.type_to_object[type_]

class VisualLine(IByPointDraw):
    def __init__(self, line: Line, visual_plane: VisualPlane, color: tuple):
        super().__init__(line)
        self.line = line
        self.color = color
        self.type_ = VisualLine.type_
        self.visual_plane = visual_plane
        width, height = visual_plane.plane.size()
        if line.angle != 90:
            for x in range(width*10):
                round_x = round(x/10)
                round_y = round(line.get_y_coordinate(x/10))
                if 0 <= round_y < height:
                    if self.draw_coordinates.get(Point(round_x, round_y), None) == None:
                        self.draw_coordinates[Point(round_x, round_y)] = self.color
        else:
            round_x = round(line.sample_coordinates.x)
            for y in range(height):
                if self.draw_coordinates.get(Point(round_x, y), None) == None:
                    self.draw_coordinates[Point(round_x, y)] = self.color
        self.visual_plane.bind_object(self)


class VisualPoint(IByPointDraw):
    def __init__(self, point: Point, visual_plane: VisualPlane, color: tuple):
        super().__init__(point)
        self.point = point
        self.color = color
        self.visual_plane = visual_plane
        self.draw_coordinates[Point(round(point.x), round(point.y))] = self.color
        self.type_ = IByPointDraw.type_
        self.visual_plane.bind_object(self)


class VisualLineSegment(IByPointDraw):
    def __init__(self, line_segment: LineSegment, visual_plane: VisualPlane, color: tuple):
        super().__init__(line_segment)
        self.line_segment = line_segment
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)
        self.type_ = IByPointDraw.type_

        width, height = self.visual_plane.plane.size()
        if self.line_segment.endpoints[0].x != self.line_segment.endpoints[1].x:
            for x in range(round(self.line_segment.endpoints[0].x)*100, round(self.line_segment.endpoints[1].x)*100):
                round_x = round(x/100)
                round_y = round(self.line_segment.reconstruct_line().get_y_coordinate(x/100))
                if 0 <= round_y < height and 0 <= round_x < width:
                        if self.draw_coordinates.get(Point(round_x, round_y), None) == None:
                            self.draw_coordinates[Point(round_x, round_y)] = self.color
        else:
            round_x = round(self.line_segment.endpoints[0].x)
            min_y = min(round(self.line_segment.endpoints[0].y), round(self.line_segment.endpoints[1].y))
            max_y = max(round(self.line_segment.endpoints[0].y), round(self.line_segment.endpoints[1].y))
            for y in range(min_y, max_y+1):
                if 0 <= y < height and 0 <= round_x < width:
                        if self.draw_coordinates.get(Point(round_x, y), None) == None:
                            self.draw_coordinates[Point(round_x, y)] = self.color


class VisualPolygon(IByPointDraw):
    def __init__(self, polygon: Polygon, visual_plane: VisualPlane, color: tuple):
        super().__init__(polygon)
        self.polygon = polygon
        self.type_ = IByPointDraw.type_
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)

        for x in range(round(polygon.min_x), round(polygon.max_x)+1):
            for y in range(round(polygon.min_y), round(polygon.max_y)+1):
                point = Point(x, y)
                if polygon.is_point_inside(point) and self.draw_coordinates.get(point, None) == None:
                    self.draw_coordinates[point] = self.color