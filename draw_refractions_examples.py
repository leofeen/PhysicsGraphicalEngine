from optical.opticalfigures import RefractionPolygon
from visual.visual2d import VisualPlane, Color
from plane.plane2d import Point
from optical.opticallines import RefractionLine, ReflectionSegment
from optical.light_beam import LightBeam
from visual.visuallight import LightBeamSceneManager


def draw_refractions_example():
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

    IMAGE_GROUPS = {
        'Refractions example': {
            'beams': BEAMS,
            'lines': LINES,
            'line_segments': LINE_SEGMENTS,
        },
        'Prism example': {
            'beams': BEAMS,
            'polygons': POLYGONS,
            'lines': LINES,
        },
    }

    scene = LightBeamSceneManager(plane, image_groups=IMAGE_GROUPS)
    
    scene.draw_all_images()


if __name__ == '__main__':
    draw_refractions_example()