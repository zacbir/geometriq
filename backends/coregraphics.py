from datetime import datetime

from .quartz import *
from .base_canvas import BaseCanvas

from ..shapes import origin


class ContextTranslator:

    def __init__(self, context, translation_point):
        self.context = context
        self.translation_point = translation_point

    def __enter__(self):
        CGContextTranslateCTM(self.context, self.translation_point.x, self.translation_point.y)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        CGContextTranslateCTM(self.context, -self.translation_point.x, -self.translation_point.y)


class ContextRotator:

    def __init__(self, context, rotation):
        self.context = context
        self.rotation = rotation

    def __enter__(self):
        CGContextRotateCTM(self.context, self.rotation)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        CGContextRotateCTM(self.context, -self.rotation)


class CoreGraphicsCanvas(BaseCanvas):
    def __init__(self, name, width, height=None):
        height = height if height else width
        super(CoreGraphicsCanvas, self).__init__(name, width, height)

        self.colorSpace = CGColorSpaceCreateDeviceRGB()
        self.context = CGBitmapContextCreate(None, width, height, 8, width * 4, self.colorSpace, kCGImageAlphaPremultipliedLast)
        self.path = None

    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width
        CGContextSetLineWidth(self.context, self.stroke_width)

    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color
        CGContextSetRGBStrokeColor(self.context, *self.stroke_color.rgba())

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        CGContextSetRGBFillColor(self.context, *self.fill_color.rgba())

    def fill_background(self):
        r = CGRect((0, 0), (self.width, self.height))
        CGContextAddRect(self.context, r)
        CGContextDrawPath(self.context, kCGPathFillStroke)

    def draw_line(self, from_point, to_point, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                path = CGPathCreateMutable()
                CGPathMoveToPoint(path, None, from_point.x, from_point.y)
                CGPathAddLineToPoint(path, None, to_point.x, to_point.y)
                CGContextAddPath(r_t_context, path)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_polygon(self, points, at_point=origin, rotation=0):
        drawn_points = points[:]
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                path = CGPathCreateMutable()
                starting_point = drawn_points.pop(0)
                CGPathMoveToPoint(path, None, starting_point.x, starting_point.y)
                for next_point in drawn_points:
                    CGPathAddLineToPoint(path, None, next_point.x, next_point.y)
                CGPathAddLineToPoint(path, None, starting_point.x, starting_point.y)
                CGContextAddPath(r_t_context, path)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_circle(self, radius, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                path = CGPathCreateMutable()
                CGContextAddEllipseInRect(r_t_context,
                                          CGRect((origin.x - radius, origin.y - radius), (radius * 2, radius * 2)))
                CGContextAddPath(r_t_context, path)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_quarter_circle(self, radius, at_point=origin, rotation=0):
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
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                offset = (4 * radius * (sqrt(2) - 1)) / 3

                path = CGPathCreateMutable()
                # Heavy lifting
                CGContextAddPath(r_t_context, path)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_half_circle(self, radius, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                path = CGPathCreateMutable()
                # Heavy lifting
                CGContextAddPath(r_t_context, path)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}_{}.png".format(self.name, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)


