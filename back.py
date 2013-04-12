import sys
from PIL import Image

img = Image.open(sys.argv[1] + '.png')

w = int(sys.argv[2])
h = img.size[1]

for i in range(img.size[0] / w):
    box = (i * w, 0, (i + 1) * w, h)
    
    tmp = img.crop(box)
    tmp = tmp.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(tmp, box)

img.save(sys.argv[1] + '_back.png', "PNG")
