from opticalfigures import RefractionPolygon
from visual2d import VisualPlane, Color
from plane2d import Point
from opticallines import RefractionLine, ReflectionSegment
from light_beam import LightBeam
from visuallight import LightBeamSceneManager

plane = VisualPlane(1000, path_to_image_folder='./refractions')

LINE_SEGMENTS = [
    (ReflectionSegment(Point(410, 290), Point(520, 120), 0.3), Color.MAGENTA),
]

LINES = [
    (RefractionLine(Point(500, 500), 1, 1.6, -50), Color.GREEN),
]

POLYGONS = [
    (RefractionPolygon([Point(410, 290), Point(520, 120), Point(390, 120)], 1.6, 2.1, transparensy=0.8), Color.GREEN),
]

BEAMS = [
    (LightBeam(Point(700, 700), -120), Color.RED, True),
    (LightBeam(Point(300, 300), 85), Color.BLUE, True),
]

scene = LightBeamSceneManager(plane, lines=LINES, beams=BEAMS, line_segments=LINE_SEGMENTS)
scene.draw_picture('Refractions example')

scene.regroup_scene(beams=BEAMS, polygons=POLYGONS, lines=LINES)
scene.draw_picture('Prism example')