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
    percentile = float((value - lower_bounds) / (upper_bounds - lower_bounds))
    idx = round(percentile * (len(iterable) - 1))
    return iterable[idx]
