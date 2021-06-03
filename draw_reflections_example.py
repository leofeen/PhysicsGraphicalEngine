from visual2d import VisualPlane, Color
from plane2d import Point
from opticallines import ReflectionLine
from light_beam import LightBeam
from visuallight import LightBeamSceneManager

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
    (ReflectionLine(Point(750, 750), 0.5, 80), Color.BLUE),
]

BEAMS = [
    (LightBeam(Point(700, 700), -120), Color.RED, True),
    (LightBeam(Point(300, 300), 85), Color.PURPLE, True),
]

scene = LightBeamSceneManager(plane, lines=LINES, beams=BEAMS, points=POINTS)

scene.draw_picture()