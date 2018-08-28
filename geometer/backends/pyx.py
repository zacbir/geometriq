import pyx

from ..canvas import Canvas


class PyxCanvas(Canvas):

    def __init__(self, name, width, height):
        super(PyxCanvas, self).__init__(name, width, height)
