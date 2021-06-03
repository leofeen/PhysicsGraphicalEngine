from typing import Iterable
from PIL import Image, ImageDraw
from plane2d import Line, Plane, Point


class Color:
    #TODO: add more colors
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 0, 90)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    LIGHT_BLUE = (0, 255, 255)
    WHITE = (255, 255, 255)
    LIGHT_GREEN = (0, 255, 90)
    PURPLE = (90, 0, 255)
    BLACK = (0, 0, 0)

    @staticmethod
    def blend_colors(first_color, second_color, t):
        new_red = pow((1 - t)*(first_color[0]**2) + t*(second_color[0]**2), 1/2)
        new_green = pow((1 - t)*(first_color[1]**2) + t*(second_color[1]**2), 1/2)
        new_blue = pow((1 - t)*(first_color[2]**2) + t*(second_color[2]**2), 1/2)
        return (round(new_red), round(new_green), round(new_blue))


class IByPointDraw:
    type_ = 0
    def __init__(self):
        IByPointDraw.type_ += 1
        self.type = IByPointDraw.type_
        self.draw_coordinates = {}
        self.color = (0, 0, 0, 0)

    def get_color_on_point(self, coordinates: Point):
        return self.draw_coordinates.get(Point(coordinates[0], coordinates[1]), self.color)


class VisualPlane:
    def __init__(self, width=None, height=None, *, plane: Plane=None, path_to_image_folder=None, background_color=Color.BLACK):
        #TODO: intersects_with - stop drawing after collision
        if plane == None:
            self.plane = Plane(width, height)
        else:
            self.plane = plane
        self.image_counter = 0
        self.color = (0, 0, 0, 255)
        self.type_to_object = {0: self}
        if path_to_image_folder == None:
            self.path_to_image_folder = './imgs'
        else:
            self.path_to_image_folder = path_to_image_folder
        self.background_color = background_color

    def create_image(self):
        image = Image.new('RGB', self.plane.size())
        image_draw = ImageDraw.ImageDraw(image)
        width, height = self.plane.size()
        for x in range(width):
            for y in range(height-1, -1, -1):
                image_draw.point((x, y), self.type_to_object[self.plane.get_point(Point(x, height - 1 - y))].get_color_on_point((x, height - 1 - y)))
        image.save(f'{self.path_to_image_folder}/image{self.image_counter}.png')
        self.image_counter += 1

    def bind_object(self, obj:IByPointDraw):
        if self.type_to_object.get(obj.type_, None) == None:
            self.type_to_object[obj.type_] = obj
        else:
            raise KeyError(f'Type {obj.type_} already binded to a color')

    def draw_object_by_point(self, obj: IByPointDraw):
        for coordinates in obj.draw_coordinates:
            self.plane.set_point(coordinates, obj.type_)

    def draw_by_coordinates(self, coordinates_iter: Iterable[Point], type_):
        for coordinates in coordinates_iter:
            self.plane.set_point(coordinates, type_)

    def get_color_on_point(self, point: Point):
        return self.background_color

class VisualLine(IByPointDraw):
    def __init__(self, line: Line, visual_plane: VisualPlane, color: tuple):
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
        super().__init__()
        self.point = point
        self.color = color
        self.visual_plane = visual_plane
        self.draw_coordinates[Point(round(point.x), round(point.y))] = self.color
        self.type_ = IByPointDraw.type_
        self.visual_plane.bind_object(self)