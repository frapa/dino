import sys
import os
import cairo
import rsvg

name = sys.argv[1]

files = []
for filename in os.listdir('./'):
    if filename.find(name) != -1 and filename.find('.svg') != -1:
        files.append(filename)
        
img = cairo.ImageSurface(cairo.FORMAT_ARGB32, len(files) * int(sys.argv[2]), int(sys.argv[3]))
ctx = cairo.Context(img)

for f in sorted(files):
    print f
    handler = rsvg.Handle(f)
    handler.render_cairo(ctx)
    ctx.translate(int(sys.argv[2]), 0)

img.write_to_png(name + ".png")
