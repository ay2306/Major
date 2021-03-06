from os import listdir,getcwd
from os.path import isfile, join
import cv2
import matplotlib.pyplot as plt
import imagehash
from PIL import Image, ImageFilter,UnidentifiedImageError
import random
import art
import json
import numpy
import scipy.fftpack
import pywt
output_stream = open("./graphs/src/data/whash.json","w")

print(art.text2art("aHash"))

class Loader:
    def __init__(self,name,total):
        self.latest = -1
        self.loaderLength = 0
        self.name = name
        self.total = int(total)

    def calculate(self,current):
        return current/self.total*100
    
    def printLoader(self,current):
        # print(current,self.calculate(current),self.total)
        current = self.calculate(current)
        if int(current) > self.latest:
            self.latest = int(current)
            toPrint = f"\r{'#'*self.latest}{'.'*(100-self.latest)}   {self.latest}% {self.name} completed"
            print(toPrint, end="")
            self.loaderLength = len(toPrint)
    
    def removeLoader(self):
        print("")
    

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


def whash(image):
    hash_size = 8
    image_natural_scale = 2**int(numpy.log2(min(image.size)))
    image_scale = max(image_natural_scale, hash_size)
    ll_max_level = int(numpy.log2(image_scale))
    level = int(numpy.log2(hash_size))
    dwt_level = ll_max_level - level
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (image_scale,image_scale),
        Image.ANTIALIAS,
    )
    pixels = []
    for row in range(image_scale):
        cur_row = []
        for col in range(image_scale):
            cur_row.append(image.getpixel((col,row))/255)
        pixels.append(cur_row)
    coeffs = pywt.wavedec2(pixels, 'haar', level = ll_max_level)
    coeffs = list(coeffs)
    coeffs[0] *= 0
    pixels = pywt.waverec2(coeffs, 'haar')
    # print("pixel",pixels)
    
    coeffs = pywt.wavedec2(pixels, 'haar', level = dwt_level)
    dwt_low = coeffs[0]
    median = numpy.median(dwt_low)

    # print("pixel",len(pixels),"X",len(pixels[0]));
    # print("coeff",len(coeffs),"X",len(coeffs[0]));
    # print("median",median)
    # print("dwt",len(dwt_low),"X",len(dwt_low[0]));
    difference = []
    # print("dwt low",dwt_low)
    for row in range(hash_size):
        for col in range(hash_size):
            current_pixel = dwt_low[row][col]
            difference.append(current_pixel >= median)
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

imageLoadingLoader = Loader("Image Loading",len(files))
index = 0
for file in files:
    index += 1
    imageLoadingLoader.printLoader(index)
    try:
        path = join(getcwd(),IMAGES,file)
        image = Image.open(path)
        data.append({
            "path" : file,
            "hash" : int(whash(image),16)
        })
        # exit(0)
    except UnidentifiedImageError:
        pass
imageLoadingLoader.removeLoader()

all_match = {}
result = {}
row = len(data)

# output_stream.write(json.dumps(data))
# exit(0)
imageProcessingLoader = Loader("Image Processing",row*(row-1))
for i in range(row):
    for j in range(i+1,row):
        imageProcessingLoader.printLoader(i*row+j+1)
        lev = diff(data[i]["path"],data[j]["path"])
        match = calculateMatch(data[i]["hash"],data[j]["hash"])
        # print(lev,match,data[i]["path"],data[j]["path"])
        if lev not in result:
            result[lev] = {}
        if match not in result[lev]:
            result[lev][match] = 0
        result[lev][match] += 1
        if match not in all_match:
            all_match[match] = 1

imageProcessingLoader.removeLoader()


for lev in result:
    for match in all_match:
        if match not in result[lev]:
            result[lev][match] = 0


for lev in result:
    # print(lev)
    data = []
    for match in result[lev]:
        data.append((match,result[lev][match]))
    result[lev] = sorted(data)

output_stream.write(json.dumps(result))