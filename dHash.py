from os import listdir,getcwd
from os.path import isfile, join
import cv2
import matplotlib.pyplot as plt
import imagehash
from PIL import Image, ImageFilter,UnidentifiedImageError
import random

def hammingDistance(n1, n2) :
    x = n1 ^ n2 
    setBits = 0
    while (x > 0) :
        setBits += x & 1
        x >>= 1
    return setBits 

def diff(a,b):
    level = 3
    a = a.split('_')
    b = b.split('_')
    for i in range(3):
        if a[i] != b[i]:
            break
        else:
            level -= 1
    return f"Level {level}"

def calculateMatch(a,b):
    BITS = 64
    return round((BITS-hammingDistance(a,b))/BITS*100,2)


def dhash2(image):
    hash_size = 8
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )
    pixels = list(image.getdata())
    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

IMAGES = "img"
files = [x for x in listdir(IMAGES) if isfile(join(IMAGES,x))]
data = []
for file in files:
    try:
        path = join(getcwd(),IMAGES,file)
        image = Image.open(path)
        data.append({
            "path" : file,
            "hash" : int(dhash2(image),16)
        })
    except UnidentifiedImageError:
        pass
result = {}
for i in range(len(data)):
    for j in range(i+1,len(data)):
        lev = diff(data[i]["path"],data[j]["path"])
        match = calculateMatch(data[i]["hash"],data[j]["hash"])
        if lev not in result:
            result[lev] = {}
        if match not in result[lev]:
            result[lev][match] = 0
        result[lev][match] += 1

for lev in sorted(result):
    print(lev)
    for match in sorted(result[lev]):
        print(f"\t{match} : {result[lev][match]}")