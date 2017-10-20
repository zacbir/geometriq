#from ctypes import *
from array import array
import os.path

from .backends.quartz import *
from .colors import Color
from .shapes import Point


class ReferenceImage(object):

    data_provider_func = {
        '.png': CGImageCreateWithPNGDataProvider,
        '.jpg': CGImageCreateWithJPEGDataProvider,
        '.JPG': CGImageCreateWithJPEGDataProvider,
        '.jpeg': CGImageCreateWithJPEGDataProvider,
    }

    def __init__(self, image_path, canvas):
        self.canvas = canvas
        data_provider = CGDataProviderCreateWithFilename(os.path.expanduser(image_path))
        ext = os.path.splitext(image_path)[-1].lower()
        image_func = self.data_provider_func[ext]
        self.image = image_func(data_provider, None, False, kCGRenderingIntentDefault)
        self.width = CGImageGetWidth(self.image)
        self.height = CGImageGetHeight(self.image)
        color_space = CGColorSpaceCreateDeviceRGB()
        self.bytes_per_pixel = 4
        self.bytes_per_row = self.bytes_per_pixel * self.width
        bits_per_component = 8
        # self.raw_data = (c_byte * self.width * self.height * self.bytes_per_pixel)()
        self.raw_data = array('B', (0 for i in range(self.width * self.height * self.bytes_per_pixel)))
        context = CGBitmapContextCreate(self.raw_data, self.width, self.height, bits_per_component, self.bytes_per_row,
                                        color_space, kCGImageAlphaPremultipliedLast)
        CGContextDrawImage(context, CGRect((0, 0), (self.width, self.height)), self.image)

    def transform_point(self, point, crop=False):
        """
        Currently assumes our canvas and our image share an aspect ratio, better transforms TK
        """
        from_width, from_height = float(self.canvas.width), float(self.canvas.height)
        to_width, to_height = float(self.width), float(self.height)
        from_aspect = float(from_width) / from_height
        to_aspect = float(to_width) / to_height
        return Point(point.x * (to_width / from_width), point.y * (to_height / from_height))

    def color_at_point(self, point):
        x, y = int(point.x), int(point.y)
        translated_y = (self.height - 1) - y
        byte_index = int((self.bytes_per_row * translated_y) + (x * self.bytes_per_pixel))
        try:
            red, green, blue, alpha = self.raw_data[byte_index:byte_index + 4]
        except ValueError:  # out of the images bounds, hand back clear
            red = green = blue = alpha = 0.0

        return Color.from_full_value(red, green, blue, alpha)

    def image_matrix(self):
        pixels = []
        rows = []
        for i in range(len(self.raw_data) / self.bytes_per_pixel):
            idx = i * self.bytes_per_pixel
            r = self.raw_data[idx]
            g = self.raw_data[idx + 1]
            b = self.raw_data[idx + 2]
            a = self.raw_data[idx + 3]
            pixels.append(Color.from_full_value(r, g, b, a))

            for j in range(len(pixels) / self.width):
                idx = j * self.width
                rows.append(pixels[idx:idx + self.width])

        return rows
