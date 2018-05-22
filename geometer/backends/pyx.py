import pyx

from .base_canvas import BaseCanvas


class PyxCanvas(BaseCanvas):

    def __init__(self, name, width, height):
        super(PyxCanvas, self).__init__(name, width, height)
