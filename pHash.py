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
output_stream = open("./graphs/src/data/pHash.json","w")

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


def phash(image):
    hash_size = 8
    freq = 4
    img_size = hash_size*freq
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (img_size, img_size),
        Image.ANTIALIAS,
    )
    pixels = []
    for row in range(img_size):
        cur_row = []
        for col in range(img_size):
            cur_row.append(image.getpixel((col,row)))
        pixels.append(cur_row)
    # print(pixels)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis = 0), axis = 1)
    # print(dct)
    dct = dct[:hash_size,:hash_size]
    median = numpy.median(dct)
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            current_pixel = dct[row][col]
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
            "hash" : int(phash(image),16)
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