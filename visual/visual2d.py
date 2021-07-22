from math import fabs
from typing import Any, Iterable, Optional
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw

from plane.plane2d import Cirlce, Line, LineSegment, Plane, Point, Polygon, Vector2d

ColorType = tuple[int, int, int]


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
    def blend_colors(first_color: ColorType, second_color: ColorType, blending_coefficient: float) -> ColorType:
        """
        Blends two given colors and returns resulting colors.
        Blending coefficient determines how much second color will affect first.
        If blenging coefficient equals to 0, first color will be returned.
        If blenging coefficient equals to 1, second color will be returned. 
        """
        if not (0 <= blending_coefficient <= 1):
            raise ValueError(f'Blending coefficient must be in [0; 1], but {blending_coefficient} was given')

        new_red = pow((1 - blending_coefficient)*(first_color[0]**2) + blending_coefficient*(second_color[0]**2), 1/2)
        new_green = pow((1 - blending_coefficient)*(first_color[1]**2) + blending_coefficient*(second_color[1]**2), 1/2)
        new_blue = pow((1 - blending_coefficient)*(first_color[2]**2) + blending_coefficient*(second_color[2]**2), 1/2)
        return (round(new_red), round(new_green), round(new_blue))


class Drawable(ABC):
    _draw_id = 0

    def __init__(self):
        self.draw_coordinates: dict[Point, ColorType] = {}
        Drawable._draw_id += 1
        self.draw_id = Drawable._draw_id

    def get_draw_coordinates(self) -> dict[Point, ColorType]:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        return self.draw_coordinates

    @abstractmethod
    def get_color_on_point(self, point: Point, precision: Optional[float]) -> ColorType:
        pass

    @abstractmethod
    def compute_draw_coordinates(self) -> None:
        pass

    @abstractmethod
    def get_transparensy(self) -> float:
        pass


class DrawableSet:
    """
    Set-like object with interface for accessing objects by their draw_id.
    """

    def __init__(self, *args) -> None:
        self.__set: set[Drawable] = set(args)

    def __getitem__(self, draw_id: int):
        list_of_objects = [x for x in self.__set if x.draw_id == draw_id]
        if len(list_of_objects) != 1:
            raise KeyError(draw_id)
        return list_of_objects[0]

    def add(self, obj: Drawable):
        """
        Adds element to set.

        This has no effect if the element is already present.
        """
        self.__set.add(obj)

    def remove(self, obj: Drawable):
        """
        Remove an element from a set; it must be a member.

        If the element is not a member, raise a KeyError.
        """
        self.__set.remove(obj)


class VisualPlane(Drawable):
    def __init__(self, width: int = None, height: int = None, *, plane: Plane = None,
                 path_to_image_folder: str = '', background_color: ColorType = Color.BLACK) -> None:
        if plane is None:
            self.plane = Plane(width, height)
        else:
            self.plane = plane
        self.image_counter = 0
        if path_to_image_folder == '':
            self.path_to_image_folder = '.'
        else:
            self.path_to_image_folder = path_to_image_folder
        self.background_color = background_color
        self.objects_on_plane = DrawableSet(self)
        self.draw_id = 0
        self.draw_coordinates = {}

    def compute_draw_coordinates(self) -> None:
        width, height = self.plane.size()
        for x in range(width):
            for y in range(height):
                point = Point(x, y)
                self.draw_coordinates[point] = self.get_color_on_point(point)

    def get_color_on_point(self, point: Point, precision: Optional[float] = None) -> ColorType:
        object_on_point = self.objects_on_plane[self.plane.get_point(point)]
        if object_on_point == self:
            return self.background_color
        if precision is None:
            return object_on_point.get_color_on_point(point)
        else:
            return object_on_point.get_color_on_point(point, precision)

    def get_transparensy(self) -> int:
        return 1

    def flip_point_horizontally(self, point: Point) -> Point:
        _, height = self.plane.size()
        x, y = point.as_tuple()
        return Point(x, height - y - 1)

    def create_image(self, image_name: str = '') -> None:
        image = Image.new('RGB', self.plane.size())
        image_draw = ImageDraw.ImageDraw(image)
        
        draw_coordinates = self.get_draw_coordinates()
        for point in draw_coordinates:
            image_draw.point(self.flip_point_horizontally(point).as_tuple(), draw_coordinates[point])
        if image_name == '':
            image.save(f'{self.path_to_image_folder}/image{self.image_counter}.png')
        else:
            image.save(f'{self.path_to_image_folder}/{image_name}.png')
        self.image_counter += 1

    def bind_object(self, obj: Drawable) -> None:
        self.objects_on_plane.add(obj)

    def draw_object_by_point(self, obj: Drawable) -> None:
        for coordinates in obj.get_draw_coordinates():
            self.plane.set_point(coordinates, obj.draw_id)

    def draw_by_coordinates(self, coordinates_iter: Iterable[Point], draw_id: int) -> None:
        for coordinates in coordinates_iter:
            self.plane.set_point(coordinates, draw_id)

    def reset_plane(self) -> None:
        width, height = self.plane.size()
        self.plane = Plane(width, height)
        self.objects_on_plane = DrawableSet(self)
        self.draw_coordinates = {}

    def get_value_on_point(self, point: Point) -> int:
        return self.plane.get_point(point)

    def get_binded_object(self, draw_id: int) -> Drawable:
        return self.objects_on_plane[draw_id]

class VisualLine(Drawable):
    def __init__(self, line: Line, visual_plane: VisualPlane, color: ColorType) -> None:
        super().__init__()
        self.line = line
        self.color = color
        self.visual_plane = visual_plane
        self.get_transparensy = getattr(self.line, 'get_transparensy', lambda: 0)
        self.visual_plane.bind_object(self)
        self.compute_draw_coordinates()

    def get_transparensy(self) -> float:
        pass

    def get_color_on_point(self, point: Point, precision: float = 0.1) -> ColorType:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        if point in self.draw_coordinates.keys():
            return self.draw_coordinates[point]
        elif fabs(self.line.get_y_coordinate(point.x) - point.y) < precision:
            return self.color
        else:
            return Color.NONE

    def compute_draw_coordinates(self) -> None:
        width, height = self.visual_plane.plane.size()
        if self.line.angle != 90:
            number_of_trials = round(fabs(self.line.angle_coefficient))+1 if fabs(self.line.angle_coefficient) >= 1 else 1
            for x in range(width*number_of_trials):
                round_x = round(x/number_of_trials)
                round_y = round(self.line.get_y_coordinate(x/number_of_trials))
                if 0 <= round_y < height:
                    if self.draw_coordinates.get(Point(round_x, round_y), None) is None:
                        self.draw_coordinates[Point(round_x, round_y)] = self.color
        else:
            round_x = round(self.line.sample_coordinates.x)
            for y in range(height):
                if self.draw_coordinates.get(Point(round_x, y), None) is None:
                    self.draw_coordinates[Point(round_x, y)] = self.color


class VisualPoint(Drawable):
    def __init__(self, point: Point, visual_plane: VisualPlane, color: ColorType) -> None:
        super().__init__()
        self.point = point
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)
        self.get_transparensy = getattr(self.point, 'get_transparensy', lambda: 0)
        self.compute_draw_coordinates()

    def compute_draw_coordinates(self) -> None:
        self.draw_coordinates[Point(round(self.point.x), round(self.point.y))] = self.color

    def get_color_on_point(self, point: Point, precision: float = 0.5) -> ColorType:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        if point in self.draw_coordinates.keys():
            return self.draw_coordinates[point]
        elif (fabs(point.x - self.point.x) < precision) and (fabs(point.y - self.point.y) < precision):
            return self.color
        else:
            return Color.NONE

    def get_transparensy(self) -> float:
        pass


class VisualLineSegment(Drawable):
    def __init__(self, line_segment: LineSegment, visual_plane: VisualPlane, color: ColorType) -> None:
        super().__init__()
        self.line_segment = line_segment
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)
        self.get_transparensy = getattr(self.line_segment, 'get_transparensy', lambda: 0)
        self.compute_draw_coordinates()

    def compute_draw_coordinates(self) -> None:
        width, height = self.visual_plane.plane.size()
        if self.line_segment.endpoints[0].x != self.line_segment.endpoints[1].x:
            for x in range(round(self.line_segment.endpoints[0].x)*100, round(self.line_segment.endpoints[1].x)*100):
                round_x = round(x/100)
                round_y = round(self.line_segment.reconstruct_line().get_y_coordinate(x/100))
                if 0 <= round_y < height and 0 <= round_x < width:
                        if self.draw_coordinates.get(Point(round_x, round_y), None) is None:
                            self.draw_coordinates[Point(round_x, round_y)] = self.color
        else:
            round_x = round(self.line_segment.endpoints[0].x)
            min_y = round(self.line_segment.min_y)
            max_y = round(self.line_segment.max_y)
            for y in range(min_y, max_y+1):
                if 0 <= y < height and 0 <= round_x < width:
                        if self.draw_coordinates.get(Point(round_x, y), None) is None:
                            self.draw_coordinates[Point(round_x, y)] = self.color

    def get_color_on_point(self, point: Point, precision: float = 0.2) -> ColorType:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        if point in self.draw_coordinates.keys():
            return self.draw_coordinates[point]
        elif (fabs(self.line_segment.reconstruct_line().get_y_coordinate(point.x) - point.y) < precision
                and self.line_segment.min_y <= point.y <= self.line_segment.max_y
                and self.line_segment.min_x <= point.x <= self.line_segment.max_x):
            return self.color
        else:
            return Color.NONE

    def get_transparensy(self) -> float:
        pass


class VisualPolygon(Drawable):
    def __init__(self, polygon: Polygon, visual_plane: VisualPlane, color: ColorType) -> None:
        super().__init__()
        self.polygon = polygon
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)
        self.get_transparensy = getattr(self.polygon, 'get_transparensy', lambda: 0)
        self.compute_draw_coordinates()

    def compute_draw_coordinates(self) -> None:
        for x in range(round(self.polygon.min_x), round(self.polygon.max_x)+1):
            for y in range(round(self.polygon.min_y), round(self.polygon.max_y)+1):
                point = Point(x, y)
                if self.polygon.is_point_inside(point) and self.draw_coordinates.get(point, None) is None:
                    self.draw_coordinates[point] = self.color

    def get_color_on_point(self, point: Point, precision: Optional[float] = None) -> ColorType:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        if point in self.draw_coordinates.keys():
            return self.draw_coordinates[point]
        elif self.polygon.is_point_inside(point):
            return self.color
        else:
            return Color.NONE

    def get_transparensy(self) -> float:
        pass


class VisaulCircle(Drawable):
    def __init__(self, circle: Cirlce, visual_plane: VisualPlane, color: ColorType, draw_only_circumference: bool = False) -> None:
        super().__init__()
        self.circle = circle
        self.color = color
        self.visual_plane = visual_plane
        self.visual_plane.bind_object(self)
        self.is_circumference = draw_only_circumference
        self.get_transparensy = getattr(self.circle, 'get_transparensy', lambda: 0)
        self.compute_draw_coordinates()

    def compute_draw_coordinates(self) -> None:
        if self.is_circumference:
            turn_amount = 90 / (self.circle.radius * self.circle.radius)
            angle = 0
            while angle < 360:
                vector_to_point = Vector2d.construct_from_length(self.circle.radius, angle)
                point_to_draw = self.circle.centre + vector_to_point
                self.draw_coordinates[point_to_draw] = self.color
                angle += turn_amount
        else:
            for x in range(round(self.circle.centre.x - self.circle.radius), round(self.circle.centre.x + self.circle.radius)+1):
                for y in range(round(self.circle.centre.y - self.circle.radius), round(self.circle.centre.y + self.circle.radius)+1):
                    if self.circle.centre.get_distance_to_point(Point(x, y)) <= self.circle.radius:
                        self.draw_coordinates[Point(x, y)] = self.color

    def get_color_on_point(self, point: Point, precision: Optional[float] = 0.2) -> ColorType:
        if not self.draw_coordinates:
            self.compute_draw_coordinates()
        if point in self.draw_coordinates.keys():
            return self.draw_coordinates[point]
        elif self.is_circumference and fabs(point.get_distance_to_point(self.circle.centre) - self.circle.radius) < precision:
            return self.color
        elif self.circle.is_point_inside(point) and not self.is_circumference:
            return self.color
        else:
            return Color.NONE

    def get_transparensy(self) -> float:
        pass