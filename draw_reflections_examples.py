from plane.polygons2d import Triangle
from optical.opticalfigures import ReflectionPolygon, ReflectionCircle
from visual.visual2d import VisualPlane, Color
from plane.plane2d import Point
from optical.opticallines import ReflectionLine, ReflectionSegment
from optical.light_beam import LightBeam
from visual.visuallight import LightBeamSceneManager


def draw_reflections_examples():
    plane = VisualPlane(1000, path_to_image_folder='./reflections')

    POINTS = [
        (Point(100, 100), Color.PINK),
        (Point(102, 100), Color.PINK),
        (Point(99, 99), Color.PINK),
        (Point(100, 99), Color.PINK),
        (Point(101, 99), Color.PINK),
        (Point(102, 99), Color.PINK),
        (Point(103, 99), Color.PINK),
        (Point(100, 98), Color.PINK),
        (Point(101, 98), Color.PINK),
        (Point(102, 98), Color.PINK),
        (Point(101, 97), Color.PINK),
    ]

    LINES = [
        (ReflectionLine(Point(500, 500), 1, -70), Color.GREEN),
        (ReflectionLine(Point(750, 750), 0.5, 80), Color.MAGENTA),
    ]

    SEGMENTS_REFLECTION_COEFFICIENT = 0.9
    LINE_SEGMENTS = [
        (ReflectionSegment(Point(350, 150), Point(350, 500), SEGMENTS_REFLECTION_COEFFICIENT), Color.GREEN),
        (ReflectionSegment(Point(0, 500), Point(580, 500), SEGMENTS_REFLECTION_COEFFICIENT), Color.GREEN),
        (ReflectionSegment(Point(100, 150), Point(650, 150), SEGMENTS_REFLECTION_COEFFICIENT), Color.GREEN),
        (ReflectionSegment(Point(650, 150), Point(650, 500), SEGMENTS_REFLECTION_COEFFICIENT), Color.GREEN),
        (ReflectionSegment(Point(650, 500), Point(590, 500), SEGMENTS_REFLECTION_COEFFICIENT), Color.GREEN),
    ]

    BEAMS = [
        (LightBeam(Point(700, 700), -120), Color.RED, True),
        (LightBeam(Point(300, 300), 85), Color.AQUA, True),
    ]

    BEAMS2 = [
        (LightBeam(Point(260, 900), -95), Color.RED, True),
        (LightBeam(Point(620, 870), -120), Color.BLUE, True),
    ]

    POLYGONS = [
        (ReflectionPolygon.from_polygon(Triangle.construct_by_two_sides(Point(320, 450), 150, 250, 30, 65), 1), Color.GREEN),
        (ReflectionPolygon.from_polygon(Triangle.construct_by_two_sides(Point(190, 190), 280, 330, 20, 65), 1), Color.AQUA),
        (ReflectionPolygon.from_polygon(Triangle.construct_by_two_sides(Point(420, 510), 90, 75, 40, -55), 1), Color.YELLOW),
        (ReflectionPolygon.from_polygon(Triangle.construct_by_two_sides(Point(460, 580), 90, 85, 45, -60), 1), Color.GREEN),
        (ReflectionPolygon.from_polygon(Triangle.construct_by_two_sides(Point(530, 420), 280, 150, 65, -55), 1), Color.AQUA),
        (ReflectionPolygon([Point(200, 510), Point(270, 560), Point(240, 740), Point(170, 730)], 1), Color.MAGENTA),
        (ReflectionPolygon([Point(320, 190), Point(470, 200), Point(460, 360), Point(310, 350)], 1), Color.MAGENTA),
        (ReflectionPolygon([Point(660, 700), Point(740, 660), Point(750, 760), Point(680, 790)], 1), Color.YELLOW),
    ]

    CIRCLES = [
        (ReflectionCircle(Point(760, 550), 75, 1), Color.AQUA, False),
    ]

    IMAGE_GROUPS = {
        'Reflections example': {
            'beams': BEAMS,
            'lines': LINES,
            'points': POINTS,
        },
        'Black body model': {
            'beams': BEAMS,
            'line_segments': LINE_SEGMENTS,
        },
        'Figure mirrors': {
            'beams': BEAMS2,
            'polygons': POLYGONS,
            'circles': CIRCLES,
        },
    }

    scene = LightBeamSceneManager(plane, image_groups=IMAGE_GROUPS)

    scene.draw_all_images()


if __name__ == '__main__':
    draw_reflections_examples()