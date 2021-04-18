import shutil
import os
from PIL import Image, ImageFilter
import random
import math

RAW_IMAGES = "raw_images"
IMAGES = "img"

if "raw_images" not in os.listdir(os.getcwd()):
    link = 'https://drive.google.com/drive/folders/1U982UYw8AIkWhXJVqLrl08qK8ZzBboOS?usp=sharing'
    print(f"Please download folder (link provided below) and save it as directory named 'raw_images'\nLink to folder: {link}")
    exit(0)

try:
    shutil.rmtree(IMAGES)
except FileNotFoundError:
    pass
os.mkdir(os.path.join(os.getcwd(),"img"))

def generateBlock(path):
    return {
        "path" : path 
    }

all_files = []

def getShrinkMultiplier():
    x = 10
    while not (x > 0 and x < 1):
        x = random.SystemRandom().random()
    return x

def getContent(path):
    files = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
    directory = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    for file in files:
        all_files.append(generateBlock(os.path.join(path,file)))
    for folder in directory:
        getContent(os.path.join(path,folder))

def convertToCamelCase(name):
    try:
        name = name.split('_')
    except AttributeError:
        print(name)
    x = ""
    for i in name:
        if len(x) == 0:
            x = i.lower()
        else:
            x += i[0].upper() + i[1:].lower()
    return x

def ceil(x):
    return int(math.ceil(x))

getContent(RAW_IMAGES)

done = 0
for file in all_files:
    done += 1
    p = file["path"].split('/')
    # print(p)
    # print(file["path"])
    if(len(p) == 0):
        break
    image = Image.open(os.path.join(os.getcwd(),file["path"]))
    # image.filter(ImageFilter.BLUR).show()
    # image.filter(ImageFilter.DETAIL).show()
    # image.filter(ImageFilter.EDGE_ENHANCE).show()
    # image.filter(ImageFilter.EDGE_ENHANCE_MORE).show()
    # image.filter(ImageFilter.SHARPEN).show()
    # image.filter(ImageFilter.SMOOTH).show()
    # image.filter(ImageFilter.SMOOTH_MORE).show()
    p[0] = IMAGES
    extension = "." + p[-1].split('.')[1]
    p[-1] = p[-1].split('.')[0]
    for index in range(len(p)):
        p[index] = convertToCamelCase(p[index])
    fileName = os.path.join(os.getcwd(),p[0],'_'.join(p[1:]))
    print(f"{fileName} {round(done/len(all_files)*100,2)}% completed")
    image.save(fileName+"_NORMAL"+extension)
    image.filter(ImageFilter.BLUR).save(fileName+"_BLUR"+extension)
    image.filter(ImageFilter.DETAIL).save(fileName+"_DETAIL"+extension)
    image.filter(ImageFilter.EDGE_ENHANCE).save(fileName+"_EDGE-ENHANCE"+extension)
    image.filter(ImageFilter.EDGE_ENHANCE_MORE).save(fileName+"_EDGE-ENHANCE-MORE"+extension)
    image.filter(ImageFilter.SHARPEN).save(fileName+"_SHARPEN"+extension)
    image.filter(ImageFilter.SMOOTH).save(fileName+"_SMOOTH"+extension)
    image.filter(ImageFilter.SMOOTH_MORE).save(fileName+"_SMOOTH-MORE"+extension)
    image.resize((ceil(image.size[0]*getShrinkMultiplier()), ceil(image.size[1]*getShrinkMultiplier()))).save(fileName+"_SHRUNK"+extension)