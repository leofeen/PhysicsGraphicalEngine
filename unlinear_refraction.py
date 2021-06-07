import math

from visual2d import VisualPlane, Color
from plane2d import Point
from opticallines import RefractionLine
from light_beam import LightBeam
from visuallight import LightBeamSceneManager


def equation(x: float):
    return 2 + math.sin(2*x) # 2 added to shift result in range [1; 3]

plane = VisualPlane(1000, path_to_image_folder='./unlinear_refractions')

BEAMS = [
    (LightBeam(Point(100, 900), -45), Color.RED, True),
]

lines = []

STARTING_HEIGHT = 700
previous_refraction_coefficient = 1
for depth in range(STARTING_HEIGHT, 0, -2):
    new_refraction_coefficient = equation((STARTING_HEIGHT - depth)/100)
    lines.append((RefractionLine(Point(500, depth), previous_refraction_coefficient, new_refraction_coefficient, 0), (0, 0, 150)))
    previous_refraction_coefficient = new_refraction_coefficient

scene = LightBeamSceneManager(plane, beams=BEAMS, lines=lines, refraction_coefficients_management=False)
scene.draw_picture('Sine equation')