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
        self.rotation = radians(rotation)

    def __enter__(self):
        CGContextRotateCTM(self.context, self.rotation)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        CGContextRotateCTM(self.context, -self.rotation)


class ContextScalor:

    def __init__(self, context, scale_x, scale_y=None):
        self.context = context
        self.scale_x = scale_x
        self.scale_y = scale_y if scale_y is not None else scale_x

    def __enter__(self):
        CGContextScaleCTM(self.context, self.scale_x, self.scale_y)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        CGContextScaleCTM(self.context, 1 / self.scale_x, 1 / self.scale_y)


def call_decorator(f):

    def log_and_call(*args, **kw):
        # args_join = ", ".join([repr(x) for x in args[1:]])
        # kw_join = ", ".join(['{}={}'.format(repr(k), repr(v)) for (k, v) in kw.items()])

        # args[0].log("canvas.{}({}{})".format(f.__name__, args_join, ", {}".format(kw_join) if kw_join else ""))

        return f(*args, **kw)

    return log_and_call


class CoreGraphicsCanvas(BaseCanvas):

    def __init__(self, name, width, height=None, debug=False):
        height = height if height else width
        super(CoreGraphicsCanvas, self).__init__(name, width, height)

        self.colorSpace = CGColorSpaceCreateDeviceRGB()
        self.context = CGBitmapContextCreate(None, width, height, 8, width * 4, self.colorSpace, kCGImageAlphaPremultipliedLast)

        self.debug = debug
        self.operation_count = 0

        self.log_file = "{}.log".format(self.name)

        self.log("canvas = {}({}, {}, {})".format(self.__class__.__name__, repr(name), repr(width), repr(height)))

    def log(self, msg):
        with open(self.log_file, 'a+') as log:
            log.write("{}\n".format(msg))

    @call_decorator
    def set_line_join(self, join_style):
        self.join_style = join_style
        CGContextSetLineJoin(self.context, self.join_style)

    @call_decorator
    def set_line_cap(self, cap_style):
        self.cap_style = cap_style
        CGContextSetLineCap(self.context, self.cap_style)

    @call_decorator
    def set_miter_limit(self, miter_limit):
        self.miter_limit = miter_limit
        CGContextSetMiterLimit(self.context, self.miter_limit)

    @call_decorator
    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width
        CGContextSetLineWidth(self.context, self.stroke_width)

    @call_decorator
    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color
        CGContextSetRGBStrokeColor(self.context, *self.stroke_color.rgba())

    @call_decorator
    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        CGContextSetRGBFillColor(self.context, *self.fill_color.rgba())

    @call_decorator
    def fill_background(self):
        r = CGRect((0, 0), (self.width, self.height))
        CGContextAddRect(self.context, r)
        CGContextDrawPath(self.context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def draw_line(self, from_point, to_point, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextMoveToPoint(r_t_context, from_point.x, from_point.y)
                    CGContextAddLineToPoint(r_t_context, to_point.x, to_point.y)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def draw_arc(self, radius, angle, center, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextAddArc(r_t_context, center.x, center.y, radius, 0, radians(angle), 0)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def draw_polygon(self, points, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        drawn_points = points[:]
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    starting_point = drawn_points.pop(0)
                    CGContextMoveToPoint(r_t_context, starting_point.x, starting_point.y)
                    for next_point in drawn_points:
                        CGContextAddLineToPoint(r_t_context, next_point.x, next_point.y)
                    CGContextAddLineToPoint(r_t_context, starting_point.x, starting_point.y)
                    CGContextClosePath(r_t_context)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def draw_circle(self, radius, center,  at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextAddEllipseInRect(r_t_context,
                                              CGRect((center.x - radius, center.y - radius), (radius * 2, radius * 2)))
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def draw_circular_segment(self, radius, angle, center, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextMoveToPoint(r_t_context, center.x, center.y)
                    CGContextAddLineToPoint(r_t_context, center.x + radius, center.y)
                    CGContextAddArc(r_t_context, center.x, center.y, radius, 0, radians(angle), 0)
                    CGContextAddLineToPoint(r_t_context, center.x, center.y)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @call_decorator
    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}{}.png".format(self.name, "-{:05}".format(self.operation_count) if self.debug else "")
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)
        return filename

