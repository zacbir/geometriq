import canvas as pythonista_canvas

from .base_canvas import BaseCanvas


class PythonistaCanvas(BaseCanvas):
    def __init__(self, name, width, height):
        super(PythonistaCanvas, self).__init__(name, width, height)
        self.canvas = pythonista_canvas
        self.current_point = None

    def set_stroke_width(self, stroke_width):
        self.stroke_width = stroke_width
        self.canvas.set_line_width(self.stroke_width)

    def set_stroke_color(self, stroke_color):
        self.stroke_color = stroke_color
        self.canvas.set_stroke_color(*self.stroke_color.rgba())

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        self.canvas.set_fill_color(*self.fill_color.rgba())

    def fill_background(self):
        self.begin_path()
        self.canvas.add_rect(0, 0, self.width, self.height)
        self.canvas.fill_path()
        self.end_path()

    def begin_path(self):
        self.canvas.begin_path()

    def end_path(self):
        self.canvas.close_path()
        self.canvas.fill_path()
        self.canvas.draw_path()

    def move_to(self, point):
        self.current_point = point
        self.canvas.move_to(point.x, point.y)

    def draw_line_to(self, point):
        self.canvas.draw_line(self.current_point.x, self.current_point.y, point.x, point.y)

    def polygon(self, points):
        self.begin_path()
        self.move_to(points[0])
        for point in points[1:]:
            self.draw_line_to(point)
            self.move_to(point)
        self.end_path()

    def draw_circle(self, center, radius):
        self.canvas.fill_ellipse(center.x - radius, center.y - radius, radius * 2, radius * 2)
        self.canvas.draw_ellipse(center.x - radius, center.y - radius, radius * 2, radius * 2)

    def save(self):
        self.canvas.end_updates()
