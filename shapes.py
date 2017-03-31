from math import sqrt

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

    def distance_to(self, other_point):
        return sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

    def __repr__(self):
        return u'<Point x: {}, y: {}>'.format(self.x, self.y)

    def __key(self):
        return (self.x - 0, self.y - 0)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash(self.__key())


class Shape(object):

    """ A generic model for a regular polygon. Has a center Point(), and a
    size (though this is immaterial if its points are formed arbitrarily.

    >>> center = Point(1, 1)
    >>> s1 = Shape(center, 2)
    >>> p1 = Point(2, 1)
    >>> s1.add_point(p1)
    >>> s1.points
    [<Point x: 2, y: 1>]
    """

    def __init__(self, center, size, grid=None):
        self.center = center
        self.size = size
        self.grid = grid
        self.points = []

    def paths(self):
        paths = []

        for i in range(len(self.points)):
            p1 = self.points[i]
            idx_next = i + 1 if i + 1 < len(self.points) else 0
            p2 = self.points[idx_next]
            paths.append((p1, p2))

        return paths

    def add_point(self, point):
        if self.grid:
            point = self.grid.closest_point_to(point)
        self.points.append(point)

    def draw(self, canvas):
        canvas.polygon(self.points)


class QuarterCircle(Shape):

    def __init__(self, center, size):
        super(QuarterCircle, self).__init__(center, size)

        self.offset = (4.0 * size * (sqrt(2) - 1)) / 3.0


class NorthwestQuarterCircle(QuarterCircle):
    pass


class NortheastQuarterCircle(QuarterCircle):
    pass


class SoutheastQuarterCircle(QuarterCircle):
    pass


class SouthwestQuarterCircle(QuarterCircle):
    pass


class HalfCircle(QuarterCircle):
    """

    for i in xrange(blits):
        for j in xrange(blits - 1):
            if i % 2 == 0:
                p1 = Point(x + ((i + 1) * step), y + (j * step))
                p2 = Point(x + (i * step), y + (j * step) + step)
                p3 = Point(x + ((i + 1) * step), y + (j * step) + 2 * step)
                pointsmap = {p1 : {'point': p2,
                                   'cp1': Point(p1.x - offset, p1.y),
                                   'cp2': Point(p2.x, p2.y - offset)},
                             p2 : {'point': p3,
                                   'cp1': Point(p2.x, p2.y + offset),
                                   'cp2': Point(p3.x - offset, p3.y)}}
            else:
                p1 = Point(x + (i * step), y + (j * step))
                p2 = Point(x + (i * step) + step, y + (j * step) + step)
                p3 = Point(x + (i * step), y + (j * step) + 2 * step)
                pointsmap = {p1 : {'point': p2,
                                   'cp1': Point(p1.x + offset, p1.y),
                                   'cp2': Point(p2.x, p2.y - offset)},
                             p2 : {'point': p3,
                                   'cp1': Point(p2.x, p2.y + offset),
                                   'cp2': Point(p3.x + offset, p3.y)}}

            path = CGPathCreateMutable()
            CGContextSetRGBFillColor(ctx, 0.95, 0.85, 0.55, random.random() * 1.0)
            CGPathMoveToPoint(path, None, p1.x, p1.y)
            cp1 = pointsmap[p1]['cp1']
            cp2 = pointsmap[p1]['cp2']
            CGPathAddCurveToPoint(path, None, cp1.x, cp1.y, cp2.x, cp2.y, p2.x, p2.y)
            cp1 = pointsmap[p2]['cp1']
            cp2 = pointsmap[p2]['cp2']
            CGPathAddCurveToPoint(path, None, cp1.x, cp1.y, cp2.x, cp2.y, p3.x, p3.y)
            CGPathAddLineToPoint(path, None, p1.x, p1.y)
            CGContextAddPath(ctx, path)
            CGContextDrawPath(ctx, kCGPathFill)

    """
    pass


class NorthHalfCircle(HalfCircle):
    pass


class EastHalfCircle(HalfCircle):
    pass


class SouthHalfCircle(HalfCircle):
    pass


class WestHalfCircle(HalfCircle):
    pass


class Circle(Shape):

    def __init__(self, center, size):
        super(Circle, self).__init__(center, size)

    def draw(self, canvas):
        canvas.draw_circle(self.center, self.size)


class Triangle(Shape):

    def __init__(self, center, size, grid=None):
        super(Triangle, self).__init__(center, size, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)
        self.r = sqrt(3) * self.size / 6
        self.grid = grid

        self._setup_points()

    def _setup_points(self):
        pass


class NorthTriangle(Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.size / 2), y - self.r),
            Point(x, y + (self.step - self.r)),
            Point(x + (self.size / 2), y - self.r))]


class EastTriangle(Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - self.r, y - (self.size / 2)),
            Point(x - self.r, y + (self.size / 2)),
            Point(x + (self.step - self.r), y)
        )]


class SouthTriangle(Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in ( 
            Point(x - (self.size / 2), y + self.r),
            Point(x + (self.size / 2), y + self.r),
            Point(x, y - (self.step - self.r))
        )]


class WestTriangle(Triangle):

    def _setup_points(self):
        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - (self.step - self.r), y),
            Point(x + self.r, y + (self.size / 2)),
            Point(x + self.r, y - (self.size / 2))
        )]


class Square(Shape):

    def __init__(self, center, size):
        super(Square, self).__init__(center, size)

        x, y, sz = self.center.x, self.center.y, size / 2

        [self.add_point(x) for x in (
            Point(x - sz, y - sz),
            Point(x - sz, y + sz),
            Point(x + sz, y + sz),
            Point(x + sz, y - sz))]


class Diamond(Shape):

    def __init__(self, center, size):
        super(Diamond, self).__init__(center, size)

        self.step = sqrt(self.size**2 / 2)

        x, y = self.center.x, self.center.y

        [self.add_point(x) for x in (
            Point(x - self.step, y),
            Point(x, y + self.step),
            Point(x + self.step, y),
            Point(x, y - self.step))]


class Hexagon(Shape):

    def __init__(self, center, size, grid=None):
        super(Hexagon, self).__init__(center, size, grid)

        self.step = sqrt(self.size**2 - (self.size / 2)**2)

        self._setup_points()

    def _setup_points(self):
        pass


class HorizontalHexagon(Hexagon):

    def _setup_points(self):

        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            Point(x + sz, y + self.step),
            Point(x + self.size, y),
            Point(x + sz, y - self.step),
            Point(x - sz, y - self.step),
            Point(x - self.size, y),
            Point(x - sz, y + self.step)
        )]


class VerticalHexagon(Hexagon):

    def _setup_points(self):

        x, y, sz = self.center.x, self.center.y, self.size / 2

        [self.add_point(x) for x in (
            Point(x, y + self.size),
            Point(x + self.step, y + sz),
            Point(x + self.step, y - sz),
            Point(x, y - self.size),
            Point(x - self.step, y - sz),
            Point(x - self.step, y + sz)
        )]


triangles = [NorthTriangle, EastTriangle, SouthTriangle, WestTriangle]

squares = [Square, Diamond]

hexagons = [HorizontalHexagon, VerticalHexagon]

