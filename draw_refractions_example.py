from visual2d import VisualPlane, Color
from plane2d import Point
from opticallines import RefractionLine
from light_beam import LightBeam
from visuallight import LightBeamSceneManager

plane = VisualPlane(1000, path_to_image_folder='./refractions')

POINTS = []

LINES = [
    (RefractionLine(Point(500, 500), 1, 1.6, -50), Color.GREEN),
]

BEAMS = [
    (LightBeam(Point(700, 700), -120, initial_refraction_coefficient=1.6), Color.RED, True),
    (LightBeam(Point(300, 300), 85), Color.PURPLE, True),
]

scene = LightBeamSceneManager(plane, lines=LINES, beams=BEAMS, points=POINTS)

scene.draw_picture()