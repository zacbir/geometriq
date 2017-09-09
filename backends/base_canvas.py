from math import sqrt
import random

from ..shapes import Point, origin


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

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    @property
    def corners(self):
        return (origin, Point(0, self.height), Point(self.width, self.height), Point(self.width, 0))
        
    @property
    def diagonal(self):
        return sqrt(self.width * self.width + self.height * self.height)
    
    def random_point(self):
        return Point(random.random() * self.width, random.random() * self.height)
        
    def longest_distance_from(self, point):
        return max([point.distance_to(x) for x in self.corners])

    def point_outside(self, point):
        return point.x < 0 or point.x > self.width or point.y < 0 or point.y > self.height

    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width

    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def fill_background(self):
        pass

    def draw_line(self, from_point, to_point, at_point, rotation):
        pass

    def draw_polygon(self, points, at_point, rotation):
        pass

    def draw_circle(self, radius, at_point, rotation):
        pass

    def draw_quarter_circle(self, radius, at_point, rotation):
        pass

    def draw_half_circle(self, radius, at_point, rotation):
        pass

    def save(self):
        pass
