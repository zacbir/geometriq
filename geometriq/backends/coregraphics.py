from .quartz import *
from ..canvas import Canvas, log_on_call

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


class CoreGraphicsCanvas(Canvas):

    def __init__(self, name, width, height=None, debug=False):
        height = height if height else width
        super(CoreGraphicsCanvas, self).__init__(name, width, height)

        self.colorSpace = CGColorSpaceCreateDeviceRGB()
        self.context = CGBitmapContextCreate(None, width, height, 8, width * 4, self.colorSpace, kCGImageAlphaPremultipliedLast)

        self.debug = debug
        self.operation_count = 0

    @log_on_call
    def set_line_join(self, join_style):
        self.join_style = join_style
        CGContextSetLineJoin(self.context, self.join_style)

    @log_on_call
    def set_line_cap(self, cap_style):
        self.cap_style = cap_style
        CGContextSetLineCap(self.context, self.cap_style)

    @log_on_call
    def set_miter_limit(self, miter_limit):
        self.miter_limit = miter_limit
        CGContextSetMiterLimit(self.context, self.miter_limit)

    @log_on_call
    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width
        CGContextSetLineWidth(self.context, self.stroke_width)

    @log_on_call
    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color
        CGContextSetRGBStrokeColor(self.context, *self.stroke_color.rgba())

    @log_on_call
    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        CGContextSetRGBFillColor(self.context, *self.fill_color.rgba())

    @log_on_call
    def fill_background(self):
        r = CGRect((0, 0), (self.width, self.height))
        CGContextAddRect(self.context, r)
        CGContextDrawPath(self.context, kCGPathFill)
        if self.debug:
            self.save()
            self.operation_count += 1

    @log_on_call
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

    @log_on_call
    def draw_curve(self, points, control_points, control_points_cubic=None, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextMoveToPoint(r_t_context, points[0].x, points[0].y)
                    point_pairs = list(zip(points[:-1], points[1:]))
                    if control_points_cubic:
                        control_point_pairs = list(zip(control_points, control_points_cubic))
                    else:
                        control_point_pairs = list(zip(control_points, [None for x in range(len(control_points))]))
                    for i, (start, end) in enumerate(point_pairs):
                        cp1, cp2 = control_point_pairs[i]
                        if cp2:
                            CGContextAddCurveToPoint(r_t_context, cp1.x, cp1.y, cp2.x, cp2.y, end.x, end.y)
                        else:
                            CGContextAddQuadCurveToPoint(r_t_context, cp1.x, cp1.y, end.x, end.y)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @log_on_call
    def draw_arc(self, radius, angle, center, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextAddArc(r_t_context, center.x, center.y, radius, 0, angle, 0)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @log_on_call
    def draw_polygon(self, points, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        drawn_points = list(points)
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

    @log_on_call
    def draw_polycurves(self, curves, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        pass

    @log_on_call
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

    @log_on_call
    def draw_circular_segment(self, radius, angle, center, at_point=origin, rotation=0, scale_x=1, scale_y=None):
        with ContextScalor(self.context, scale_x, scale_y) as s_context:
            with ContextTranslator(s_context, at_point) as t_context:
                with ContextRotator(t_context, rotation) as r_t_context:
                    CGContextMoveToPoint(r_t_context, center.x, center.y)
                    CGContextAddLineToPoint(r_t_context, center.x + radius, center.y)
                    CGContextAddArc(r_t_context, center.x, center.y, radius, 0, angle, 0)
                    CGContextAddLineToPoint(r_t_context, center.x, center.y)
                    CGContextDrawPath(r_t_context, kCGPathFillStroke)
        if self.debug:
            self.save()
            self.operation_count += 1

    @log_on_call
    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}{}.png".format(self.name, "-{:05}".format(self.operation_count) if self.debug else "")
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)
        return filename

