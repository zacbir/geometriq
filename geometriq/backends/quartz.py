try:
    from Quartz.CoreGraphics import *
    from Quartz.ImageIO import *
except ImportError:
    from ._quartz import *
