#!/usr/bin/env python3
import sys
try:
    import PIL
except ModuleNotFoundError:
    print('Requires Pillow - python3 -m pip install --upgrade Pillow')
    sys.exit(1)
from PIL import Image
try:
    import numpy as np
except ModuleNotFoundError:
    print('Requires numpy - python3 -m pip install --upgrade numpy')
    sys.exit(1)
from numpy import asarray
import base64
import json
import argparse
"""
GurgleApps.com code to convert images to various formats to use in code for screens
"""
#print('Pillow Version:', PIL.__version__)

# image path to 2d array of 0 & 1s
def imageToArray(path,verbose,invert):
    image = Image.open(path)
    if verbose:
        print("Image format: ",image.format)
        print("Image size: ",image.size)
    gray = image.convert('L')
    bw = np.asarray(gray).copy()
    if invert:
        bw[bw < 128] = 1   
        bw[bw >= 128] = 0 
    else:
        bw[bw < 128] = 0    # Black
        bw[bw >= 128] = 1 # White
    data = asarray(bw)
    return data

# 2d array of 0 & 1s turned into 2d array of bytes
def bytesFromBits(bitArray):
    dataBytes = []
    for i, line in enumerate(bitArray):
        newLine = []
        for x in range(0, len(line), 8):
            byte = 0
            for n, bit in enumerate(line[x:x+8]):
                if bit == 1:
                    byte += 2**(7-n)
            newLine.append(byte)
        dataBytes.append(newLine)
    return dataBytes

# 2d array of bytes turned into our format a bytearray 1st 2 bytes width and height
def customImageFormat(byteArray):
    height = len(byteArray)
    width = len(byteArray[0]) * 8
    byteList = [width,height]
    for i, line in enumerate(byteArray):
        for n, byte in enumerate(line):
            byteList.append(byte)
    return bytearray(byteList)


def doStuff(imagePath,verbose,invert):
    if verbose:
        print('Converting '+imagePath)
    data = imageToArray(imagePath,verbose,invert)
    ###
    np.set_printoptions(threshold=np.inf)
    print("2D bit array")
    print(np.array2string(data,separator=','))
    #
    dataBytes = bytesFromBits(data)
    print("Byte Array (Horizontal)")
    print(dataBytes)
    bArray = customImageFormat(dataBytes)
    print('CUSTOM Base64 encoded with 1st 2 bytes width & height then bytes')
    #dataStr = json.dumps(dataBytes)
    #print('json')
    #print(dataStr)
    encoded = base64.b64encode(bArray)
    print(encoded)
    #print(bytearray(base64.b64decode(encoded)))

parser = argparse.ArgumentParser(description='Images to bits, bytes, code, and more ... ')
parser.add_argument("imagePath",help="path to the input image to convert")
parser.add_argument("-v",action="store_true",help="Verbose output")
parser.add_argument("-i",action="store_true",help="Invert")
args = parser.parse_args()
doStuff(args.imagePath,args.v,args.i)
