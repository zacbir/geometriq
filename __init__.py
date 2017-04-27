from .backends import *
from .colors import *
from .grids import *
try:
	from .reference_image import *
except ImportError:
	pass
from .shapes import *
from .solarized import *


def band(iterable, value, upper_bounds, lower_bounds=0):
    v = float(value)
    u_b = float(upper_bounds)
    l_b = float(lower_bounds)
    percentile = (v - l_b) / (u_b - l_b)
    idx = int(round(percentile * (len(iterable) - 1)))
    idx = 0 if idx < 0 else idx
    idx = -1 if idx >= len(iterable) else idx
    return iterable[idx]
