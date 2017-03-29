from ctypes import *
from ctypes import util

from objc_util import *

if sizeof(c_size_t) == 8:
    CFFloat = c_double
else:
    CFFloat = c_float

quartz = c

##############
# Constants
#

kCGColorSpaceSRGB = ObjCInstance(c_void_p.in_dll(quartz, 'kCGColorSpaceSRGB'))
kCGImageAlphaPremultipliedLast = 1
kCGPathFillStroke = 3
kCGRenderingIntentDefault = 0

##############
# Functions

quartz.CFURLCreateFromFileSystemRepresentation.argtypes = [c_void_p, c_char_p, c_size_t, c_bool]

quartz.CGBitmapContextCreate.restype = c_void_p
quartz.CGBitmapContextCreate.argtypes = [c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_size_t]  #

quartz.CGImageSourceCreateImageAtIndex.restype = c_void_p
quartz.CGImageSourceCreateImageAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGColorSpaceCreateDeviceRGB.restype = c_void_p
quartz.CGColorSpaceCreateDeviceRGB.argtypes = []

quartz.CGColorSpaceCreateWithName.restype = c_void_p
quartz.CGColorSpaceCreateWithName.argtypes = [c_void_p]

quartz.CGContextAddEllipseInRect.argtypes = [c_void_p, CGRect]

quartz.CGContextAddPath.argtypes = [c_void_p, c_void_p]

quartz.CGContextAddRect.argtypes = [c_void_p, CGRect]

quartz.CGContextDrawImage.restype = None
quartz.CGContextDrawImage.argtypes = [c_void_p, CGRect, c_void_p]

quartz.CGContextSetLineWidth.argtypes = [c_void_p, CFFloat]

quartz.CGContextSetRGBFillColor.argtypes = [c_void_p, CFFloat, CFFloat, CFFloat, CFFloat]

quartz.CGContextSetRGBStrokeColor.argtypes = [c_void_p, CFFloat, CFFloat, CFFloat, CFFloat]

quartz.CGDataProviderCreateWithFilename.restype = c_void_p
quartz.CGDataProviderCreateWithFilename.argtypes = [c_char_p]  # Double check

quartz.CGImageCreateWithJPEGDataProvider.restype = c_void_p
quartz.CGImageCreateWithJPEGDataProvider.argtypes = [c_void_p, CFFloat, c_bool, c_size_t]  # Double check

quartz.CGImageCreateWithPNGDataProvider.restype = c_void_p
quartz.CGImageCreateWithPNGDataProvider.argtypes = [c_void_p, CFFloat, c_bool, c_size_t]  # Double check

quartz.CGImageDestinationAddImage.argtypes = [c_void_p, c_void_p, c_void_p]  # Double check

quartz.CGImageDestinationFinalize.restype = c_bool
quartz.CGImageDestinationFinalize.argtypes = [c_void_p]

quartz.CGImageGetHeight.restype = c_size_t
quartz.CGImageGetHeight.argtypes = [c_void_p]

quartz.CGImageGetWidth.restype = c_size_t
quartz.CGImageGetWidth.argtypes = [c_void_p]

quartz.CGPathAddLineToPoint.argtypes = [c_void_p, c_void_p, CFFloat, CFFloat]

quartz.CGPathCreateMutable.restype = c_void_p

quartz.CGPathMoveToPoint.argtypes = [c_void_p, c_void_p, CFFloat, CFFloat]

CFURLCreateFromFileSystemRepresentation = quartz.CFURLCreateFromFileSystemRepresentation
CGBitmapContextCreate = quartz.CGBitmapContextCreate
CGBitmapContextCreateImage = quartz.CGBitmapContextCreateImage
CGColorSpaceCreateDeviceRGB = quartz.CGColorSpaceCreateDeviceRGB
CGColorSpaceCreateWithName = quartz.CGColorSpaceCreateWithName
CGContextAddEllipseInRect = quartz.CGContextAddEllipseInRect
CGContextAddPath = quartz.CGContextAddPath
CGContextAddRect = quartz.CGContextAddRect
CGContextDrawImage = quartz.CGContextDrawImage
CGContextSetLineWidth = quartz.CGContextSetLineWidth
CGContextSetRGBFillColor = quartz.CGContextSetRGBFillColor
CGContextSetRGBStrokeColor = quartz.CGContextSetRGBStrokeColor
CGDataProviderCreateWithFilename = quartz.CGDataProviderCreateWithFilename
CGImageCreateWithJPEGDataProvider = quartz.CGImageCreateWithJPEGDataProvider
CGImageCreateWithPNGDataProvider = quartz.CGImageCreateWithPNGDataProvider
CGImageDestinationAddImage = quartz.CGImageDestinationAddImage
CGImageDestinationFinalize = quartz.CGImageDestinationFinalize
CGImageGetHeight = quartz.CGImageGetHeight
CGImageGetWidth = quartz.CGImageGetWidth
CGPathAddLineToPoint = quartz.CGPathAddLineToPoint
CGPathCreateMutable = quartz.CGPathCreateMutable
CGPathMoveToPoint = quartz.CGPathMoveToPoint


def CGImageDestinationCreateWithURL(a, b, c, d):
    # arg 2 needs to be nsstring
    quartz.CGImageDestinationCreateWithURL(a, ns(b), c, d)
