from math import sqrt
import itertools
import random


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


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
        return u'Point(x={}, y={})'.format(self.x, self.y)

    def __key(self):
        return self.x - 0, self.y - 0

    def __cmp__(self, other):
        return cmp((self.x, self.y), (other.x, other.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
    
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y
    
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y
    
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

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

    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        points_to_draw = filter(None, self.points)
        canvas.draw_polygon(points_to_draw, at_point, rotation, scale_x, scale_y)


class Line(Shape):

    @classmethod
    def from_origin_with_slope(cls, center, slope, direction=1):
        if slope is None:  # vertical line
            line = cls(Point(center.x, center.y + direction), center=center)
        elif slope == 0:  # horizontal line
            line = cls(Point(center.x + direction, center.y), center=center)
        else:
            line = cls(Point(center.x + direction, center.y + slope), center=center)

        return line
            
    def __init__(self, to_point, center=origin):
        super(Line, self).__init__(0, center)
        self.to_point = to_point
        try:
            self.slope = (self.center.y - self.to_point.y) / (self.center.x - self.to_point.x)
            self.intercept = self.center.y - (self.center.x * self.slope)
        except ZeroDivisionError:
            self.slope = None
            self.intercept = None

        if self.slope is None:
            self.inverse_slope = 0
        elif self.slope == 0:
            self.inverse_slope = None
        else:
            self.inverse_slope = -1 / self.slope

    def __repr__(self):
        return "Line({}, center={})".format(self.to_point, self.center)

    def __key(self):
        return self.slope, self.length

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.slope == other.slope

    @property
    def length(self):
        return self.center.distance_to(self.to_point)

    @property
    def midpoint(self):
        return Point((self.to_point.x + self.center.x) / 2, (self.to_point.y + self.center.y) / 2)

    def point_from_center(self, distance):
        ratio = float(distance) / self.length
        return Point(((1 - ratio) * self.center.x) + (ratio * self.to_point.x),
                     ((1 - ratio) * self.center.y) + (ratio * self.to_point.y))
    
    def intersection_with(self, other_line):
        if self.slope == other_line.slope:
            return None  # parallel

        if self.slope is None or other_line.slope is None:  # one line is vertical, the other is not
            vert = self if self.slope is None else other_line
            non = self if other_line.slope is None else other_line
            return Point(vert.center.x, non.slope * vert.center.x + non.intercept)

        if self.slope == 0 or other_line.slope == 0:  # one line is horizontal, the other is not
            horiz = self if self.slope == 0 else other_line
            non = self if other_line.slope == 0 else other_line
            return Point(((horiz.center.y - non.intercept) / non.slope), horiz.center.y)
            
        x = (other_line.intercept - self.intercept) / (self.slope - other_line.slope)
        y = self.slope * x + self.intercept
        return Point(x, y)

    def intersects(self, other_line):
        intersection = self.intersection_with(other_line)
        return self.contains(intersection)

    def extended(self):
        new_center = self.point_from_center(-1 * random.random() * 0.05 * self.length)
        new_to_point = self.point_from_center(self.length + random.random() * 0.05 * self.length)
        return self.__class__(new_to_point, new_center)

    def line_to(self, point):
        return Line.from_origin_with_slope(point, self.inverse_slope)

    def distance_to(self, point):
        perpendicular = self.line_to(point)
        return self.intersection_with(perpendicular).distance_to(point)
        
    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        canvas.draw_line(self.center, self.to_point, at_point, rotation, scale_x, scale_y)

    def contains(self, point):
        return point and isclose(self.length, point.distance_to(self.center) + point.distance_to(self.to_point))


class Edge(object):

    def __init__(self, line, opposite_point):
        self.line = line
        self.opposite_point = opposite_point

    def __repr__(self):
        return u'Edge with Line: {}, Opposite: {}'.format(self.line, self.opposite_point)


class ArbitraryTriangle(object):

    def __init__(self, points):
        self.points = (self.A, self.B, self.C) = points

        self.AB = Line(self.B, self.A)
        self.BC = Line(self.C, self.B)
        self.CA = Line(self.A, self.C)

        self.edges = [Edge(self.AB, self.C),
                      Edge(self.BC, self.A),
                      Edge(self.CA, self.B)]

    @property
    def center(self):
        return Point((self.A.x + self.B.x + self.C.x) / 3, (self.A.y + self.B.y + self.C.y) / 3)

    def __repr__(self):
        return u'Arbitrary Triangle: {}, {}, {}'.format(self.A, self.B, self.C)

    def area(self):
        return 0.5 * self.AB.length * self.AB.distance_to(self.C)

    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        points_to_draw = filter(None, self.points)
        canvas.draw_polygon(points_to_draw, at_point, rotation, scale_x, scale_y)


class Rectangle(Line):
    
    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        points = [
            self.center,
            Point(self.center.x, self.to_point.y),
            self.to_point,
            Point(self.to_point.x, self.center.y)
        ]
        canvas.draw_polygon(points, at_point, rotation, scale_x, scale_y)


class Arc(Shape):
    
    def __init__(self, size, angle, center=origin):
        super(Arc, self).__init__(size, center)
        self.angle = angle
    
    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        canvas.draw_arc(self.size, self.angle, self.center, at_point, rotation, scale_x, scale_y)


class QuarterCircle(Arc):

    def __init__(self, size, center=origin):
        super(QuarterCircle, self).__init__(size, 90, center)


class HalfCircle(Arc):

    def __init__(self, size, center=origin):
        super(HalfCircle, self).__init__(size, 180, center)


class CircleSegment(Shape):

    def __init__(self, size, angle, center=origin):
        super(CircleSegment, self).__init__(size, center)
        self.angle = angle

    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        canvas.draw_circular_segment(self.size, self.angle, self.center, at_point, rotation, scale_x, scale_y)


class QuarterCircleSegment(CircleSegment):

    def __init__(self, size, center=origin):
        super(QuarterCircleSegment, self).__init__(size, 90, center)


class HalfCircleSegment(CircleSegment):

    def __init__(self, size, center=origin):
        super(HalfCircleSegment, self).__init__(size, 180, center)


class Circle(Shape):

    def __init__(self, size, center=origin):
        super(Circle, self).__init__(size, center)

    def draw(self, canvas, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        canvas.draw_circle(self.size, self.center, at_point, rotation, scale_x, scale_y)


class _Triangle(Shape):

    def __init__(self, size, center=origin, grid=None):
        super(_Triangle, self).__init__(size, center, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)
        self.r = sqrt(3) * self.size / 6

        self._setup_points()

    def _setup_points(self):
        pass

    @property
    def edges(self):
        A, B, C = self.points
        AB = Line(B, A)
        BC = Line(C, B)
        CA = Line(A, C)

        return [Edge(AB, C), Edge(BC, A), Edge(CA, B)]


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
