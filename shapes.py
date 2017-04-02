from math import sqrt, cos, sin, radians
import itertools

"""
Simple geometric shape models.

>>> Point(1, 1)
<Point x: 1, y: 1>
>>> p1 = Point(2, 2)
>>> p2 = Point(3, 2)
>>> p1.distance_to(p2)
1.0
"""


class Point(object):

    """ A simple two-dimensional point. Has an x value and a y value, and can
    compute the distance to another point.

    >>> p1 = Point(1, 1)
    >>> p2 = Point(2, 1)
    >>> p1.distance_to(p2)
    1.0
    >>> p1.distance_to(Point(2, 2)) == sqrt(2)
    True
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inverse(self):
        return Point(-self.x, -self.y)

    def distance_to(self, other_point):
        return sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

    def __repr__(self):
        return u'<Point x: {}, y: {}>'.format(self.x, self.y)

    def __key(self):
        return self.x - 0, self.y - 0

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash(self.__key())


origin = Point(0, 0)


class Shape(object):

    """ A generic model for a regular polygon. Has a center Point(), and a
    size (though this is immaterial if its points are formed arbitrarily.

    >>> center = Point(1, 1)
    >>> s1 = Shape(2)
    >>> p1 = Point(2, 1)
    >>> s1.add_point(p1)
    >>> s1.points
    [<Point x: 2, y: 1>]
    """

    def __init__(self, size, grid=None):
        self.center = origin
        self.size = size
        self.grid = grid
        self.points = []

    def paths(self):
        paths = []

        end_points = self.points[:]
        end_points.append(end_points.pop(0))
        return itertools.izip(self.points, end_points)

    def add_point(self, point):
        if self.grid:
            point = self.grid.closest_point_to(point)
        self.points.append(point)

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_polygon(self.points, at_point, rotation)


class QuarterCircle(Shape):

    def __init__(self, size):
        super(QuarterCircle, self).__init__(size)

        self.first_point = Point(self.center.x + size, self.center.y)

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_quarter_circle(self.size, at_point, rotation)


class HalfCircle(QuarterCircle):

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_half_circle(self.size, at_point, rotation)


class Circle(Shape):

    def __init__(self, size):
        super(Circle, self).__init__(size)

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_circle(self.size, at_point, rotation)


class Triangle(Shape):

    def __init__(self, size, grid=None):
        super(Triangle, self).__init__(size, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)
        self.r = sqrt(3) * self.size / 6

        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.size / 2), y - self.r),
            Point(x, y + (self.step - self.r)),
            Point(x + (self.size / 2), y - self.r))]


class Square(Shape):

    def __init__(self, size):
        super(Square, self).__init__(size)

        x, y, sz = self.center.x, self.center.y, size / 2

        [self.add_point(x) for x in (
            Point(x - sz, y - sz),
            Point(x - sz, y + sz),
            Point(x + sz, y + sz),
            Point(x + sz, y - sz))]


class Hexagon(Shape):

    def __init__(self, size, grid=None):
        super(Hexagon, self).__init__(size, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)

        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            Point(x + sz, y + self.step),
            Point(x + self.size, y),
            Point(x + sz, y - self.step),
            Point(x - sz, y - self.step),
            Point(x - self.size, y),
            Point(x - sz, y + self.step)
        )]
