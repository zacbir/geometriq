from ctypes import *
from ctypes import util

from objc_util import *

if sizeof(c_size_t) == 8:
    CGFloat = c_double
else:
    CGFloat = c_float

quartz = c

CGBitmapInfo = c_uint32  # CGImage.h
CGLineCap = c_int32  # CGPath.h
CGLineJoin = c_int32  # CGPath.h
CGPathDrawingMode = c_int32  # CGContext.h
CGColorRenderingIntent = c_int32  # CGColorSpace.h

class CGPoint(Structure):
    _fields_ = [
        ('x', CGFloat),
        ('y', CGFloat)
    ]

class CGSize(Structure):
    _fields_ = [
        ('width', CGFloat),
        ('height', CGFloat)
    ]

class CGRect(Structure):
    _fields_ = [
        ('origin', CGPoint),
        ('size', CGSize)
    ]

##############
# Constants
#

kCGColorSpaceSRGB = ObjCInstance(c_void_p.in_dll(quartz, 'kCGColorSpaceSRGB'))
kCGImageAlphaPremultipliedLast = 1
kCGPathFillStroke = 3
kCGRenderingIntentDefault = 0
kCGLineJoinMiter = 0
kCGLineJoinRound = 1
kCGLineJoinBevel = 2
kCGLineCapButt = 0
kCGLineCapRound = 1
kCGLineCapSquare = 2

##############
# Functions

quartz.CFURLCreateFromFileSystemRepresentation.restype = c_void_p
quartz.CFURLCreateFromFileSystemRepresentation.argtypes = [c_void_p, c_char_p, c_size_t, c_bool]

quartz.CGBitmapContextCreate.restype = c_void_p
quartz.CGBitmapContextCreate.argtypes = [c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo]

quartz.CGBitmapContextCreateImage.restype = c_void_p
quartz.CGBitmapContextCreateImage.argtypes = [c_void_p]

quartz.CGColorSpaceCreateDeviceRGB.restype = c_void_p
quartz.CGColorSpaceCreateDeviceRGB.argtypes = []

quartz.CGColorSpaceCreateWithName.restype = c_void_p
quartz.CGColorSpaceCreateWithName.argtypes = [c_void_p]

quartz.CGContextAddArc.argtypes = [c_void_p, CGFloat, CGFloat, CGFloat, CGFloat, CGFloat, c_int]

quartz.CGContextAddCurveToPoint.argtypes = [c_void_p, CGFloat, CGFloat, CGFloat, CGFloat, CGFloat, CGFloat]

quartz.CGContextAddEllipseInRect.argtypes = [c_void_p, CGRect]  # Double check

quartz.CGContextAddLineToPoint.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGContextAddQuadCurveToPoint.argtypes = [c_void_p, CGFloat, CGFloat, CGFloat, CGFloat]

quartz.CGContextAddRect.argtypes = [c_void_p, CGRect]  # Double check

quartz.CGContextClosePath.argtypes = [c_void_p]

quartz.CGContextConvertPointToDeviceSpace.restype = CGPoint
quartz.CGContextConvertPointToDeviceSpace.argtypes = [c_void_p, CGPoint]

quartz.CGContextDrawImage.argtypes = [c_void_p, CGRect, c_void_p]  # Double check

quartz.CGContextDrawPath.argtypes = [c_void_p, CGPathDrawingMode]

quartz.CGContextMoveToPoint.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGContextRotateCTM.argtypes = [c_void_p, CGFloat]

quartz.CGContextScaleCTM.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGContextSetLineCap.argtypes = [c_void_p, CGLineCap]

quartz.CGContextSetLineJoin.argtypes = [c_void_p, CGLineJoin]

quartz.CGContextSetLineWidth.argtypes = [c_void_p, CGFloat]

quartz.CGContextSetMiterLimit.argtypes = [c_void_p, CGFloat]

quartz.CGContextSetRGBFillColor.argtypes = [c_void_p, CGFloat, CGFloat, CGFloat, CGFloat]

quartz.CGContextSetRGBStrokeColor.argtypes = [c_void_p, CGFloat, CGFloat, CGFloat, CGFloat]

quartz.CGContextTranslateCTM.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGDataProviderCreateWithFilename.restype = c_void_p
quartz.CGDataProviderCreateWithFilename.argtypes = [c_char_p]

quartz.CGImageCreateWithJPEGDataProvider.restype = c_void_p
quartz.CGImageCreateWithJPEGDataProvider.argtypes = [c_void_p, POINTER(CGFloat), c_bool, CGColorRenderingIntent]

quartz.CGImageCreateWithPNGDataProvider.restype = c_void_p
quartz.CGImageCreateWithPNGDataProvider.argtypes = [c_void_p, POINTER(CGFloat), c_bool, CGColorRenderingIntent]

quartz.CGImageDestinationAddImage.argtypes = [c_void_p, c_void_p, c_void_p]

quartz.CGImageDestinationCreateWithURL.restype = c_void_p
quartz.CGImageDestinationCreateWithURL.argtypes = [c_void_p, c_void_p, c_size_t, c_void_p]

quartz.CGImageDestinationFinalize.restype = c_bool
quartz.CGImageDestinationFinalize.argtypes = [c_void_p]

quartz.CGImageGetHeight.restype = c_size_t
quartz.CGImageGetHeight.argtypes = [c_void_p]

quartz.CGImageGetWidth.restype = c_size_t
quartz.CGImageGetWidth.argtypes = [c_void_p]

CFURLCreateFromFileSystemRepresentation = quartz.CFURLCreateFromFileSystemRepresentation
CGColorSpaceCreateDeviceRGB = quartz.CGColorSpaceCreateDeviceRGB
CGColorSpaceCreateWithName = quartz.CGColorSpaceCreateWithName
CGContextAddArc = quartz.CGContextAddArc
CGContextAddCurveToPoint = quartz.CGContextAddCurveToPoint
CGContextAddEllipseInRect = quartz.CGContextAddEllipseInRect
CGContextAddLineToPoint = quartz.CGContextAddLineToPoint
CGContextAddQuadCurveToPoint = quartz.CGContextAddQuadCurveToPoint
CGContextAddRect = quartz.CGContextAddRect
CGContextClosePath = quartz.CGContextClosePath
CGContextConvertPointToToDeviceSpace = quartz.CGContextConvertPointToDeviceSpace
CGContextDrawImage = quartz.CGContextDrawImage
CGContextDrawPath = quartz.CGContextDrawPath
CGContextMoveToPoint = quartz.CGContextMoveToPoint
CGContextRotateCTM = quartz.CGContextRotateCTM
CGContextScaleCTM = quartz.CGContextScaleCTM
CGContextSetLineCap = quartz.CGContextSetLineCap
CGContextSetLineJoin = quartz.CGContextSetLineJoin
CGContextSetLineWidth = quartz.CGContextSetLineWidth
CGContextSetMiterLimit = quartz.CGContextSetMiterLimit
CGContextSetRGBFillColor = quartz.CGContextSetRGBFillColor
CGContextSetRGBStrokeColor = quartz.CGContextSetRGBStrokeColor
CGContextTranslateCTM = quartz.CGContextTranslateCTM
CGImageDestinationAddImage = quartz.CGImageDestinationAddImage
CGImageDestinationFinalize = quartz.CGImageDestinationFinalize
CGImageGetHeight = quartz.CGImageGetHeight
CGImageGetWidth = quartz.CGImageGetWidth


def CGImageDestinationCreateWithURL(a, b, c, d):
    # arg 2 needs to be nsstring
    return quartz.CGImageDestinationCreateWithURL(a, ns(b), c, d)

def CGBitmapContextCreate(a, b, c, d, e, f, g):
    return ObjCInstance(quartz.CGBitmapContextCreate(a, b, c, d, e, f, g))

def CGBitmapContextCreateImage(a):
    return ObjCInstance(quartz.CGBitmapContextCreateImage(a))

def CGDataProviderCreateWithFilename(a):
    return ObjCInstance(quartz.CGDataProviderCreateWithFilename(a.encode()))

def CGImageCreateWithJPEGDataProvider(a, b, c, d):
    return ObjCInstance(quartz.CGImageCreateWithJPEGDataProvider(a, b, c, d))
    
def CGImageCreateWithPNGDataProvider(a, b, c, d):
    return ObjCInstance(quartz.CGImageCreateWithPNGDataProvider(a, b, c, d))

