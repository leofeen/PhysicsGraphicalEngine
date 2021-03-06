from math import sin, cos, radians, asin, degrees
from typing import Union

from plane.plane2d import Cirlce, Line, LineSegment, Point
from optical.opticallines import ReflectionLine, RefractionLine

class LightBeam:
    def __init__(self, start_coordinates: Point, angle: float,
                 *,initial_refraction_coefficient: float = 1, max_bounces: int = 100) -> None:
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
        self.origin = start_coordinates
        self.initial_angle = angle

    def propogate(self, distance: float = 1) -> Point:
        if self._number_of_bounces > self.max_number_of_bounces: return

        previous_x, previous_y = self.coordinates[-1].x, self.coordinates[-1].y
        x = previous_x + (cos(radians(self.angle)) * distance)
        y = previous_y + (sin(radians(self.angle)) * distance)
        self.coordinates.append(Point(x, y))
        return Point(x, y)

    def propogate_until(self, objects: list[Union[LineSegment, Line, Cirlce]]) -> Line:
        if self._number_of_bounces > self.max_number_of_bounces: return None

        starting_directions = []
        for i, object_ in enumerate(objects):
            if isinstance(object_, Line) or isinstance(object_, Cirlce):
                starting_directions.append(object_.get_direction_to_point(self.coordinates[-1]))
            elif isinstance(object_, LineSegment):
                direction = object_.reconstruct_line().get_direction_to_point(self.coordinates[-1])
                # Exclude s direction if intersection point doesn't lie on line segment itself
                if (direction == 's' and object_.check_intersection(Line(self.coordinates[-1], self.angle))) or direction != 's':
                    starting_directions.append(direction)
                else:
                    starting_directions.append('lou')
            if starting_directions[i] == 's':
                return None
        while True:
            #TODO: optimize by propogating at steps == distance to nearest object (or similar, like check in 100 radius) 
            new_point = self.propogate()
            for i, object_ in enumerate(objects):
                if isinstance(object_, Line):
                    if object_.get_direction_to_point(new_point) != starting_directions[i]:
                        self.coordinates.pop()
                        movement_line = Line(self.coordinates[-1], self.angle)
                        intersection_point = Line.get_intersection_point(object_, movement_line)
                        if intersection_point is not None:
                            self.coordinates.append(intersection_point)
                        return object_
                elif isinstance(object_, LineSegment):
                    if object_.reconstruct_line().get_direction_to_point(new_point) != starting_directions[i]:
                        movement_line = Line(self.coordinates[-2], self.angle)
                        is_intersect, intersection_point, related_line_hit = object_.get_intersection(movement_line)
                        if is_intersect:
                            self.coordinates.pop()
                            self.coordinates.append(intersection_point)
                            return related_line_hit
                elif isinstance(object_, Cirlce):
                    if object_.get_direction_to_point(new_point) != starting_directions[i]:
                        movement_line = Line(self.coordinates[-2], self.angle)
                        is_intersect, first_point, second_point = object_.get_intersection(movement_line)
                        if is_intersect:
                            self.coordinates.pop()
                            distance_first = self.coordinates[-1].get_distance_to_point(first_point)
                            distance_second = self.coordinates[-1].get_distance_to_point(second_point)
                            if distance_first <= distance_second:
                                self.coordinates.append(first_point)
                                return object_.get_tangent_line(first_point)
                            self.coordinates.append(second_point)
                            return object_.get_tangent_line(second_point)


    def reflect(self, reflection_line: ReflectionLine) -> None:
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
        self.propogate(0.01)

    def refract(self, refraction_line: RefractionLine) -> None:
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
            self.propogate(0.01)