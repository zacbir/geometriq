from math import sqrt, radians
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

    def __cmp__(self, other):
        return cmp((self.x, self.y), (other.x, other.y))

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

    def __init__(self, size, center=origin, grid=None):
        self.center = center
        self.size = size
        self.grid = grid
        self.points = []

    def paths(self):
        end_points = self.points[:]
        end_points.append(end_points.pop(0))
        return itertools.izip(self.points, end_points)

    def add_point(self, point):
        if self.grid:
            point = self.grid.closest_point_to(point)
        self.points.append(point)

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_polygon(self.points, at_point, rotation)


class Line(Shape):

    def __init__(self, to_point, center=origin):
        super(Line, self).__init__(0, center)
        self.to_point = to_point

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_line(self.center, self.to_point, at_point, rotation)


class Arc(Shape):
    
    def __init__(self, size, angle, center=origin):
        super(Arc, self).__init__(size, center)
        self.angle = angle
    
    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_arc(self.size, self.angle, at_point, rotation)


class CircleSegment(Shape):

    def __init__(self, size, angle, center=origin):
        super(CircleSegment, self).__init__(size, center)
        self.angle = angle

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_circular_segment(self.size, self.angle, at_point, rotation)


class QuarterCircle(CircleSegment):

    def __init__(self, size, center=origin):
        super(QuarterCircle, self).__init__(size, radians(90), center)


class HalfCircle(CircleSegment):

    def __init__(self, size, center=origin):
        super(HalfCircle, self).__init__(size, radians(180), center)


class Circle(Shape):

    def __init__(self, size, center=origin):
        super(Circle, self).__init__(size, center)

    def draw(self, canvas, at_point=origin, rotation=0):
        canvas.draw_circle(self.size, at_point, rotation)


class _Triangle(Shape):

    def __init__(self, size, center=origin, grid=None):
        super(_Triangle, self).__init__(size, center, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)
        self.r = sqrt(3) * self.size / 6

        self._setup_points()

    def _setup_points(self):
        pass


class NorthTriangle(_Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.size / 2), y - self.r),
            Point(x, y + (self.step - self.r)),
            Point(x + (self.size / 2), y - self.r))]


class EastTriangle(_Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - self.r, y - (self.size / 2)),
            Point(x - self.r, y + (self.size / 2)),
            Point(x + (self.step - self.r), y))]


class SouthTriangle(_Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.size / 2), y + self.r),
            Point(x + (self.size / 2), y + self.r),
            Point(x, y - (self.step - self.r)))]


class WestTriangle(_Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.step - self.r), y),
            Point(x + self.r, y + (self.size / 2)),
            Point(x + self.r, y - (self.size / 2)))]


class HexagonalRhombus(Shape):

    def __init__(self, size, center=origin, grid=None):
        super(HexagonalRhombus, self).__init__(size, center, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)

        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            self.center,
            Point(x - self.step, y + sz),
            Point(x, y + self.size),
            Point(x + self.step, y + sz))]


class Square(Shape):

    def __init__(self, size, center=origin):
        super(Square, self).__init__(size, center)

        x, y, sz = self.center.x, self.center.y, size / 2

        [self.add_point(x) for x in (
            Point(x - sz, y - sz),
            Point(x - sz, y + sz),
            Point(x + sz, y + sz),
            Point(x + sz, y - sz))]


class Diamond(Shape):

    def __init__(self, size, center=origin):
        super(Diamond, self).__init__(size, center)
        self.step = sqrt(self.size ** 2 / 2)
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - self.step, y),
            Point(x, y + self.step),
            Point(x + self.step, y),
            Point(x, y - self.step))]


class _Hexagon(Shape):

    def __init__(self, size, center=origin, grid=None):
        super(_Hexagon, self).__init__(size, center, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)

        self._setup_points()

    def _setup_points(self):
        pass


class HorizontalHexagon(_Hexagon):

    def _setup_points(self):
        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            Point(x + sz, y + self.step),
            Point(x + self.size, y),
            Point(x + sz, y - self.step),
            Point(x - sz, y - self.step),
            Point(x - self.size, y),
            Point(x - sz, y + self.step))]


class VerticalHexagon(_Hexagon):

    def _setup_points(self):
        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            Point(x, y + self.size),
            Point(x + self.step, y + sz),
            Point(x + self.step, y - sz),
            Point(x, y - self.size),
            Point(x - self.step, y - sz),
            Point(x - self.step, y + sz))]


# Useful aliases for use with translated/rotated contexts
Triangle = NorthTriangle
Hexagon = VerticalHexagon
