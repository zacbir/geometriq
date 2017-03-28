"""

kCGColorSpaceSRGB
kCGImageAlphaPremultipliedLast
kCGPathFillStroke
kCGRenderingIntentDefault

CFURLCreateFromFileSystemRepresentation
CGBitmapContextCreate
CGBitmapContextCreateImage
CGColorSpaceCreateDeviceRGB
CGColorSpaceCreateWithName
CGContextAddEllipseInRect
CGContextAddPath
CGContextAddRect
CGContextDrawImage
CGContextDrawPath
CGContextSetLineWidth
CGContextSetRGBFillColor
CGContextSetRGBStrokeColor
CGDataProviderCreateWithFilename
CGImageCreateWithJPEGDataProvider
CGImageCreateWithPNGDataProvider
CGImageDestinationAddImage
CGImageDestinationCreateWithURL
CGImageDestinationFinalize
CGImageGetHeight
CGImageGetWidth
CGPathAddLineToPoint
CGPathCreateMutable
CGPathMoveToPoint
CGRectMake

"""

from ctypes import *
from ctypes import util

from objc_util import *

if sizeof(c_size_t)==8:
	CFFloat=c_double
else:
	CFFloat=c_float

######################################################################

# QUARTZ / COREGRAPHICS

quartz = c

CGDirectDisplayID = c_uint32  # CGDirectDisplay.h
CGError = c_int32  # CGError.h
CGBitmapInfo = c_uint32  # CGImage.h

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     ImageIO.framework/Headers/CGImageProperties.h
kCGImagePropertyGIFDictionary = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDictionary')
kCGImagePropertyGIFDelayTime = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDelayTime')

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     CoreGraphics.framework/Headers/CGColorSpace.h
kCGRenderingIntentDefault = 0

quartz.CGImageSourceCreateWithData.restype = c_void_p
quartz.CGImageSourceCreateWithData.argtypes = [c_void_p, c_void_p]

quartz.CGImageSourceCreateImageAtIndex.restype = c_void_p
quartz.CGImageSourceCreateImageAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageSourceCopyPropertiesAtIndex.restype = c_void_p
quartz.CGImageSourceCopyPropertiesAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageGetDataProvider.restype = c_void_p
quartz.CGImageGetDataProvider.argtypes = [c_void_p]

quartz.CGDataProviderCopyData.restype = c_void_p
quartz.CGDataProviderCopyData.argtypes = [c_void_p]

quartz.CGDataProviderCreateWithCFData.restype = c_void_p
quartz.CGDataProviderCreateWithCFData.argtypes = [c_void_p]

quartz.CGImageCreate.restype = c_void_p
quartz.CGImageCreate.argtypes = [c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, c_bool, c_int]

quartz.CGImageRelease.restype = None
quartz.CGImageRelease.argtypes = [c_void_p]

quartz.CGImageGetBytesPerRow.restype = c_size_t
quartz.CGImageGetBytesPerRow.argtypes = [c_void_p]

quartz.CGImageGetWidth.restype = c_size_t
quartz.CGImageGetWidth.argtypes = [c_void_p]

quartz.CGImageGetHeight.restype = c_size_t
quartz.CGImageGetHeight.argtypes = [c_void_p]

quartz.CGImageGetBitsPerPixel.restype = c_size_t
quartz.CGImageGetBitsPerPixel.argtypes = [c_void_p]

quartz.CGImageGetBitmapInfo.restype = CGBitmapInfo
quartz.CGImageGetBitmapInfo.argtypes = [c_void_p]

quartz.CGColorSpaceCreateDeviceRGB.restype = c_void_p
quartz.CGColorSpaceCreateDeviceRGB.argtypes = []

quartz.CGDataProviderRelease.restype = None
quartz.CGDataProviderRelease.argtypes = [c_void_p]

quartz.CGColorSpaceRelease.restype = None
quartz.CGColorSpaceRelease.argtypes = [c_void_p]

quartz.CGBitmapContextCreate.restype = c_void_p
quartz.CGBitmapContextCreate.argtypes = [c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo]

quartz.CGBitmapContextCreateImage.restype = c_void_p
quartz.CGBitmapContextCreateImage.argtypes = [c_void_p]

quartz.CGFontCreateWithDataProvider.restype = c_void_p
quartz.CGFontCreateWithDataProvider.argtypes = [c_void_p]

quartz.CGFontCreateWithFontName.restype = c_void_p
quartz.CGFontCreateWithFontName.argtypes = [c_void_p]

quartz.CGContextDrawImage.restype = None
quartz.CGContextDrawImage.argtypes = [c_void_p, CGRect, c_void_p]

quartz.CGContextRelease.restype = None
quartz.CGContextRelease.argtypes = [c_void_p]

quartz.CGContextSetTextPosition.restype = None
quartz.CGContextSetTextPosition.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGContextSetShouldAntialias.restype = None
quartz.CGContextSetShouldAntialias.argtypes = [c_void_p, c_bool]

#these are needed because argtypes are not all voids
quartz.CGImageDestinationCreateWithURL.argtypes=[c_void_p,c_void_p,c_int,c_void_p]
quartz.CGContextSetRGBFillColor.argtypes=[c_void_p, CFFloat, CFFloat, CFFloat, CFFloat]
quartz.CGContextSetRGBStrokeColor.argtypes=[c_void_p, CFFloat, CFFloat, CFFloat, CFFloat]
quartz.CGColorSpaceCreateWithName.argtypes=[c_void_p]
quartz.CFURLCreateFromFileSystemRepresentation.argtypes=[c_void_p,c_char_p,c_size_t,c_bool]

####################
# Exports

############
# Constants

kCGColorSpaceSRGB=ObjCInstance(c_void_p.in_dll(quartz,'kCGColorSpaceSRGB'))
kCGImageAlphaPremultipliedLast=1
kCGPathFillStroke=3
kCGRenderingIntentDefault=0

CFURLCreateFromFileSystemRepresentation = quartz.CFURLCreateFromFileSystemRepresentation
CGBitmapContextCreate = quartz.CGBitmapContextCreate
CGBitmapContextCreateImage = quartz.CGBitmapContextCreateImage
CGColorSpaceCreateDeviceRGB = quartz.CGColorSpaceCreateDeviceRGB
CGColorSpaceCreateWithName = quartz.CGColorSpaceCreateWithName
CGContextAddEllipseInRect = quartz.CGContextAddEllipseInRect
CGContextAddPath = quartz.CGContextAddPath
CGContextAddRect = quartz.CGContextAddRect
CGContextDrawImage = quartz.CGContextDrawImage
CGContextDrawPath = quartz.CGContextDrawPath
CGContextSetLineWidth = quartz.CGContextSetLineWidth
CGContextSetRGBFillColor = quartz.CGContextSetRGBFillColor
CGContextSetRGBStrokeColor = quartz.CGContextSetRGBStrokeColor
CGDataProviderCreateWithFilename = quartz.CGDataProviderCreateWithFilename
CGImageCreateWithJPEGDataProvider = quartz.CGImageCreateWithJPEGDataProvider
CGImageCreateWithPNGDataProvider = quartz.CGImageCreateWithPNGDataProvider
CGImageDestinationAddImage = quartz.CGImageDestinationAddImage
CGImageDestinationCreateWithURL = quartz.CGImageDestinationCreateWithURL
CGImageDestinationFinalize = quartz.CGImageDestinationFinalize
CGImageGetHeight = quartz.CGImageGetHeight
CGImageGetWidth = quartz.CGImageGetWidth
CGPathAddLineToPoint = quartz.CGPathAddLineToPoint
CGPathCreateMutable = quartz.CGPathCreateMutable
CGPathMoveToPoint = quartz.CGPathMoveToPoint
#CGRectMake = quartz.CGRectMake
