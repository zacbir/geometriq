from datetime import datetime

from PIL import Image, ImageDraw

from canvas import BaseCanvas
from shapes import Point


class PillowCanvas(BaseCanvas):
    def __init__(self, name, width, height):
        super(PillowCanvas, self).__init__(name, width, height)

        self.width = int(round(width * 2))
        self.height = int(round(height * 2))

        self.original_width = int(round(width))
        self.original_height = int(round(height))

        self.image = Image.new('RGBA', (self.width, self.height), None)
        self.drawer = ImageDraw.Draw(self.image, mode='RGBA')
        self.current_point = None

    def _translate_point(self, point):
        return Point(int(round(point.x * 2)), int(round((self.original_height - point.y) * 2)))

    def center(self):
        return Point(int(round(self.original_width / 2)), int(round(self.original_height / 2)))

    def set_stroke_width(self, stroke_width):
        self.stroke_width = int(round(stroke_width * 2))

    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def fill_background(self):
        p1 = self._translate_point(Point(0, 0))
        p2 = self._translate_point(Point(self.original_width, self.original_height))
        self.drawer.rectangle([(p1.x, p1.y), (p2.x, p2.y)], fill=self.fill_color.int_rgba())

    def move_to(self, point):
        self.current_point = self._translate_point(point)

    def draw_line_to(self, point):
        translated_point = self._translate_point(point)
        self.drawer.line([(self.current_point.x, self.current_point.y),
                          (translated_point.x, translated_point.y)],
                         fill=self.stroke_color.int_rgba(),
                         width=self.stroke_width)
        self.current_point = translated_point

    def polygon(self, points):
        t_points = [self._translate_point(p) for p in points]
        p_coords = [(p.x, p.y) for p in t_points]
        self.drawer.polygon(p_coords, fill=self.fill_color.int_rgba(), outline=self.stroke_color.int_rgba())

    def draw_circle(self, center, radius):
        p1 = self._translate_point(Point(center.x - radius, center.y - radius))
        p2 = self._translate_point(Point(center.x + radius, center.y + radius))
        self.drawer.fill_ellipse([(p1.x, p1.y), (p2.x, p2.y)],
                                 outline=self.stroke_color.int_rgba(),
                                 fill=self.fill_color.int_rgba())

    def save(self):
        filename = "{}{}.png".format(self.name, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        self.image = self.image.resize((self.original_width, self.original_height), resample=Image.LANCZOS)
        self.image.save(filename, 'PNG')
