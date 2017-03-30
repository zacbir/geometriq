from datetime import datetime

from .quartz import *
from .base_canvas import BaseCanvas


class CoreGraphicsCanvas(BaseCanvas):
    def __init__(self, name, width, height):
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

    def save(self):
        image = CGBitmapContextCreateImage(self.context)
        filename = "{}{}.png".format(self.name, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        url = NSURL.fileURLWithPath_(filename)
        dest = CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
        CGImageDestinationAddImage(dest, image, None)
        CGImageDestinationFinalize(dest)


