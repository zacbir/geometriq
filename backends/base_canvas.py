from ..shapes import Point


class BaseCanvas(object):
    """ An abstract canvas API providing a means to draw shapes on itself

    It is specified as a 2-dimensional area, with a width and a height.

    It can draw lines of varying thickness and color

    It can draw circles

    It can fill shapes with arbitrary color in RGB space

    Subclasses define library-specific implementations of these basic tools
    """

    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.stroke_width = None
        self.stroke_color = None
        self.fill_color = None

    def center(self):
        return Point(self.width / 2, self.height / 2)

    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width

    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def fill_background(self):
        pass

    def begin_path(self):
        pass

    def end_path(self):
        pass

    def move_to(self, point):
        pass

    def draw_line(self, from_point, to_point):
        pass

    def polygon(self, points):
        pass

    def draw_circle(self, center, radius):
        pass

    def save(self):
        pass
