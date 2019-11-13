from math import sqrt
import random

from .shapes import Point, origin


def log_on_call(f):
    def log_and_call(*args, **kw):
        args_join = ", ".join([repr(x) for x in args[1:]])
        kw_join = ", ".join(["{}={}".format(repr(k), repr(v)) for (k, v) in kw.items()])

        args[0].log(
            "canvas.{}({}{})".format(
                f.__name__, args_join, ", {}".format(kw_join) if kw_join else ""
            )
        )

        return f(*args, **kw)

    return log_and_call


class StrokeWidthContext:
    def __init__(self, canvas, stroke_width):
        self.canvas = canvas
        self.old_width = canvas.stroke_width
        self.new_width = stroke_width

    def __enter__(self):
        self.canvas.set_stroke_width(self.new_width)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.set_stroke_width(self.old_width)


class StrokeColorContext:
    def __init__(self, canvas, stroke_color):
        self.canvas = canvas
        self.old_color = canvas.stroke_color
        self.new_color = stroke_color

    def __enter__(self):
        self.canvas.set_stroke_color(self.new_color)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.set_stroke_color(self.old_color)


class FillColorContext:
    def __init__(self, canvas, fill_color):
        self.canvas = canvas
        self.old_color = canvas.fill_color
        self.new_color = fill_color

    def __enter__(self):
        self.canvas.set_fill_color(self.new_color)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.set_fill_color(self.old_color)


class Canvas(object):
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
        self.log_file = "{}.log".format(self.name)
        self.log(
            "canvas = {}({}, {}, {})".format(
                self.__class__.__name__, repr(name), repr(width), repr(height)
            )
        )

    def log(self, msg):
        with open(self.log_file, "a+") as log:
            log.write("{}\n".format(msg))

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    @property
    def corners(self):
        return (
            origin,
            Point(0, self.height),
            Point(self.width, self.height),
            Point(self.width, 0),
        )

    @property
    def diagonal(self):
        return sqrt(self.width * self.width + self.height * self.height)

    def random_point(self):
        return Point(random.random() * self.width, random.random() * self.height)

    def longest_distance_from(self, point):
        return max([point.distance_to(x) for x in self.corners])

    def point_outside(self, point):
        return (
            point.x < 0 or point.x > self.width or point.y < 0 or point.y > self.height
        )

    @log_on_call
    def set_line_join(self, join_style):
        self.join_style = join_style

    @log_on_call
    def set_line_cap(self, cap_style):
        self.cap_style = cap_style

    @log_on_call
    def set_miter_limit(self, miter_limit):
        self.miter_limit = miter_limit

    @log_on_call
    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width

    @log_on_call
    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color

    @log_on_call
    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    @log_on_call
    def fill_background(self):
        pass

    @log_on_call
    def draw_line(
        self, from_point, to_point, at_point=origin, rotation=0, scale_x=1, scale_y=None
    ):
        pass

    @log_on_call
    def draw_curve(
        self,
        points,
        control_points,
        control_points_cubic=None,
        at_point=origin,
        rotation=0,
        scale_x=1,
        scale_y=None,
    ):
        pass

    @log_on_call
    def draw_arc(
        self,
        radius,
        angle,
        center,
        at_point=origin,
        rotation=0,
        scale_x=1,
        scale_y=None,
    ):
        pass

    @log_on_call
    def draw_polygon(
        self, points, at_point=origin, rotation=0, scale_x=1, scale_y=None
    ):
        pass

    @log_on_call
    def draw_polycurves(
        self, curves, at_point=origin, rotation=0, scale_x=1, scale_y=None
    ):
        pass

    @log_on_call
    def draw_circle(
        self, radius, center, at_point=origin, rotation=0, scale_x=1, scale_y=None
    ):
        pass

    @log_on_call
    def draw_circular_segment(
        self,
        radius,
        angle,
        center,
        at_point=origin,
        rotation=0,
        scale_x=1,
        scale_y=None,
    ):
        pass

    @log_on_call
    def save(self):
        pass
