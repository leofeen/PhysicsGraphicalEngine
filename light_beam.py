from math import sin, cos, radians, asin, degrees
from plane2d import Line, Point
from opticallines import ReflectionLine, RefractionLine

class LightBeam:
    def __init__(self, start_coordinates: Point, angle: float, *, initial_refraction_coefficient: float=1, max_bounces: int=100):
        """Angle in degrees"""
        self.angle = angle
        while self.angle <= -180 or self.angle > 180:
            if self.angle < -180:
                self.angle += 360
            else:
                self.angle -= 360
        self.coordinates = [start_coordinates]
        self.refracion_coefficient = initial_refraction_coefficient
        self._number_of_bounces = 0
        self.max_number_of_bounces = max_bounces
        self.relative_intensity = 1

    def propogate(self):
        if self._number_of_bounces > self.max_number_of_bounces: return

        previous_x, previous_y = self.coordinates[-1].x, self.coordinates[-1].y
        x = previous_x + cos(radians(self.angle))
        y = previous_y + sin(radians(self.angle))
        self.coordinates.append(Point(x, y))
        return Point(x, y)

    def propogate_until(self, lines: list[Line]):
        if self._number_of_bounces > self.max_number_of_bounces: return

        starting_directions = []
        for i, line in enumerate(lines):
            starting_directions.append(line.get_direction_to_point(self.coordinates[-1]))
            if starting_directions[i] == 's':
                return None
        while True:
            #TODO: optimize by propogating at steps == distance to nearest object (or similar, like check in 100 radius) 
            new_point = self.propogate()
            for i, line in enumerate(lines):
                if line.get_direction_to_point(new_point) != starting_directions[i]:
                    self.coordinates.pop()
                    movement_line = Line(self.coordinates[-1], self.angle)
                    intersection_point = Line.get_intersection_point(line, movement_line)
                    if intersection_point != None:
                        self.coordinates.append(intersection_point)
                    return line

    def reflect(self, reflection_line: ReflectionLine):
        if self._number_of_bounces > self.max_number_of_bounces: return

        normal_line = Line.perpendicular_line(reflection_line, self.coordinates[-1])
        falling_angle = Line.angle_between(normal_line, Line(self.coordinates[-1], self.angle))
        reversed_angle = 180 + self.angle
        while not (-180 < reversed_angle <= 180):
            if reversed_angle > 180:
                reversed_angle -= 360
            else:
                reversed_angle += 360
        direction = reflection_line.get_direction_to_point(self.coordinates[-2])
        if direction == 'lou' or direction == 'rou':
            if reflection_line.angle < reversed_angle <= reflection_line.angle+90:
                new_angle = reversed_angle + 2*falling_angle
            else:
                new_angle = reversed_angle - 2*falling_angle
        else:
            if reflection_line.angle-90 <= reversed_angle < reflection_line.angle:
                new_angle = reversed_angle - 2*falling_angle
            else:
                new_angle = reversed_angle + 2*falling_angle
        while not (-180 < new_angle <= 180):
            if new_angle > 180:
                new_angle -= 360
            else:
                new_angle += 360
        self.angle = new_angle
        self._number_of_bounces += 1
        self.relative_intensity *= reflection_line.reflection_coefficient
        self.propogate()

    def refract(self, refraction_line: RefractionLine):
        if self._number_of_bounces > self.max_number_of_bounces: return
        
        direction = refraction_line.get_direction_to_point(self.coordinates[-2])
        new_refraction_coefficient = refraction_line.get_new_refraction_coefficient(direction)
        normal_line = Line.perpendicular_line(refraction_line, self.coordinates[-1])
        falling_angle = Line.angle_between(normal_line, Line(self.coordinates[-1], self.angle))
        refraction_angle_sine = (sin(radians(falling_angle)) * self.refracion_coefficient) / new_refraction_coefficient

        if refraction_angle_sine > 1:
            self.reflect(refraction_line)
        else:
            refraction_angle = degrees(asin(refraction_angle_sine))
            self.refracion_coefficient = new_refraction_coefficient
            reversed_angle = 180 + self.angle
            while not (-180 < reversed_angle <= 180):
                if reversed_angle > 180:
                    reversed_angle -= 360
                else:
                    reversed_angle += 360

            if direction == 'lou' or direction == 'rou':
                if refraction_line.angle < reversed_angle <= refraction_line.angle+90:
                    new_angle = self.angle + (falling_angle - refraction_angle)
                else:
                    new_angle = self.angle - (falling_angle - refraction_angle)
            else:
                if refraction_line.angle-90 < reversed_angle <= refraction_line.angle:
                    new_angle = self.angle + (falling_angle - refraction_angle)
                else:
                    new_angle = self.angle - (falling_angle - refraction_angle)
            while not (-180 < new_angle <= 180):
                if new_angle > 180:
                    new_angle -= 360
                else:
                    new_angle += 360
            self.angle = new_angle
            self.propogate()


if __name__ == "__main__":
    lb = LightBeam(Point(1, 1), 45)
    for _ in range(10):
        print(lb.propogate())