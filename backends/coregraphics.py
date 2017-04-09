from datetime import datetime
from math import radians

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
                CGContextMoveToPoint(r_t_context, from_point.x, from_point.y)
                CGContextAddLineToPoint(r_t_context, to_point.x, to_point.y)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_arc(self, radius, angle, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                CGContextAddArc(r_t_context, origin.x, origin.y, radius, 0, radians(angle), 0)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_polygon(self, points, at_point=origin, rotation=0):
        drawn_points = points[:]
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                starting_point = drawn_points.pop(0)
                CGContextMoveToPoint(r_t_context, starting_point.x, starting_point.y)
                for next_point in drawn_points:
                    CGContextAddLineToPoint(r_t_context, next_point.x, next_point.y)
                CGContextAddLineToPoint(r_t_context, starting_point.x, starting_point.y)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_circle(self, radius, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                CGContextAddEllipseInRect(r_t_context,
                                          CGRect((origin.x - radius, origin.y - radius), (radius * 2, radius * 2)))
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def draw_circular_segment(self, radius, angle, at_point=origin, rotation=0):
        with ContextTranslator(self.context, at_point) as t_context:
            with ContextRotator(t_context, rotation) as r_t_context:
                CGContextMoveToPoint(r_t_context, origin.x, origin.y)
                CGContextAddLineToPoint(r_t_context, origin.x + radius, origin.y)
                CGContextAddArc(r_t_context, origin.x, origin.y, radius, 0, radians(angle), 0)
                CGContextAddLineToPoint(r_t_context, origin.x, origin.y)
                CGContextDrawPath(r_t_context, kCGPathFillStroke)

    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}_{}.png".format(self.name, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)


