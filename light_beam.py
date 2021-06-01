from math import sin, cos, radians, asin, degrees
from plane2d import Line, Point

class LightBeam:
    def __init__(self, start_coordinates:Point, angle:float, initial_refraction_coefficient:float=1):
        """Angle in degrees"""
        self.angle = angle
        while self.angle < -180 or self.angle > 180:
            if self.angle < -180:
                self.angle += 360
            else:
                self.angle -= 360
        self.coordinates = [start_coordinates]
        self.refracion_coefficient = initial_refraction_coefficient

    def propogate(self):
        previous_x, previous_y = self.coordinates[-1].x, self.coordinates[-1].y
        x = previous_x + cos(radians(self.angle))
        y = previous_y + sin(radians(self.angle))
        self.coordinates.append(Point(x, y))
        return Point(x, y)

    def propogate_until(self, lines:list[Line]):
        starting_directions = []
        for i, line in enumerate(lines):
            starting_directions.append(line.get_direction_to_point(self.coordinates[-1]))
            if starting_directions[i] == 's':
                return
        while True:
            new_point = self.propogate()
            for i, line in enumerate(lines):
                if line.get_direction_to_point(new_point) != starting_directions[i]:
                    self.coordinates.pop()
                    movement_line = Line(self.coordinates[-1], self.angle)
                    intersection_point = Line.get_intersection_point(line, movement_line)
                    if intersection_point != None:
                        self.coordinates.append(intersection_point)
                    return

    def refract(self, new_refraction_coefficient:float):
        
        """new_angle = degrees(asin(self.refracion_coefficient * sin(radians(self.angle)) / new_refraction_coefficient))
        if new_angle <= 90:
            self.angle = angle
            self.refracion_coefficient = new_refraction_coefficient
        else:
            self.reflect()"""


if __name__ == "__main__":
    lb = LightBeam(Point(1, 1), 45)
    for _ in range(10):
        print(lb.propogate())