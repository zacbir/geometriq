import random
from math import sqrt


class Color(object):

    @classmethod
    def from_full_value(cls, r, g, b, a=255):
        return cls(r/255.0, g/255.0, b/255.0, a/255.0)

    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def rgba(self, a=None):
        alpha = a if a is not None else self.a
        return self.r, self.g, self.b, alpha

    def int_rgba(self):
        return int(self.r * 255.0), int(self.g * 255.0), int(self.b * 255.0), int(self.a * 255.0)

    def shade(self):
        return self.__class__(self.r, self.g, self.b, random.random() * 0.5)

    def tint(self):
        return self.__class__(self.r, self.g, self.b, 1 - random.random() * 0.5)

    def half(self):
        return self.__class__(self.r, self.g, self.b, 0.5)

    def hair(self):
        return self.__class__(self.r, self.g, self.b, 0.1)

    def alpha(self, a):
        return self.__class__(self.r, self.g, self.b, a)

    def distance_to(self, other_color):
        return sqrt((other_color.r - self.r)**2 + (other_color.g - self.g)**2 + (other_color.b - self.b)**2) # + (other_color.a - self.a)**2)

    def gradient_to(self, other_color, steps):
        for s in range(steps):
            new_r = self.r + (((other_color.r - self.r) * s) / steps)
            new_g = self.g + (((other_color.g - self.g) * s) / steps)
            new_b = self.b + (((other_color.b - self.b) * s) / steps)
            new_a = self.a + (((other_color.a - self.a) * s) / steps)
            yield self.__class__(new_r, new_g, new_b, new_a)
    
    def __repr__(self):
        return 'Color(r={}, g={}, b={}, a={})'.format(*self.rgba())


clear = Color(0, 0, 0, 0)
