from datetime import datetime

from .quartz import *
from .base_canvas import BaseCanvas


class CoreGraphicsCanvas(BaseCanvas):
    def __init__(self, name, width, height):
        super(CoreGraphicsCanvas, self).__init__(name, width, height)

        self.colorSpace = CGColorSpaceCreateDeviceRGB()
        self.context = CGBitmapContextCreate(None, width, height, 8, width * 4, self.colorSpace, kCGImageAlphaPremultipliedLast)
        self.path = None

    def translate_and_rotate_transform(self, translation_point, rotation):
        super(CoreGraphicsCanvas, self).translate_and_rotate_transform(translation_point, rotation)

        CGContextTranslateCTM(self.context, self.translation_point.x, self.translation_point.y)
        CGContextRotateCTM(self.context, self.rotation)

    def reset_transform(self):
        super(CoreGraphicsCanvas, self).reset_transform()

        CGContextRotateCTM(self.context, self.rotation)
        CGContextTranslateCTM(self.context, self.translation_point.x, self.translation_point.y)

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

    def begin_path(self):
        self.path = CGPathCreateMutable()

    def end_path(self):
        CGContextAddPath(self.context, self.path)
        CGContextDrawPath(self.context, kCGPathFillStroke)

    def move_to(self, point):
        CGPathMoveToPoint(self.path, None, point.x, point.y)

    def draw_line_to(self, point):
        CGPathAddLineToPoint(self.path, None, point.x, point.y)

    def polygon(self, points):
        self.begin_path()
        self.move_to(points[0])
        for point in points[1:]:
            self.draw_line_to(point)
        self.draw_line_to(points[0])
        self.end_path()

    def draw_circle(self, center, radius):
        self.begin_path()
        CGContextAddEllipseInRect(self.context,
                                  CGRect((center.x - radius, center.y - radius), (radius * 2, radius * 2)))
        self.end_path()

    def draw_quarter_circle(self, center, first_point):
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
        offset = (4 * radius * (sqrt(2) - 1)) / 3

        self.begin_path()
        self.end_path()

    def draw_half_circle(self, center, first_point):
        self.begin_path()
        self.end_path()

    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}{}.png".format(self.name, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)


