from plane2d import Polygon, Point


class Triangle(Polygon):
    def __init__(self, first_point: Point, second_point: Point, third_point: Point):
        super().__init__([first_point, second_point, third_point])

    #TODO: construction by sides and angles
    #TODO: class RightTriangle(point, length, angle)


#TODO: class Rectangular, etc