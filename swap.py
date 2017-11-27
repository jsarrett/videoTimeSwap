import numpy as np
import os, sys
import PIL.Image
import argparse
import mmap

out_path = "out_imgs/"
im_path = "/home/james/Pictures/timelapse/northstar_fromdeck/"
im_names = filter(lambda s: s.startswith("s") and s.endswith(".jpg"), os.listdir(im_path))
im_names.sort()
im_paths = map(lambda f: os.path.join(im_path, f), im_names)

im0 = PIL.Image.open(im_paths[0])
w,h,dur = len(im_names), im0.height, im0.width

#print w,h,t

#first make output files
out_img_files = [open(os.path.join(out_path, "%04d.raw"%i), 'wb+') for i in xrange(dur)]
for f in out_img_files:
    f.seek(3*w*h - 1)
    f.write('\x00')
    f.flush()
    f.seek(0)

out_imgs = [mmap.mmap(f.fileno(), 0) for f in out_img_files]

for col,path in enumerate(im_paths):
    print "processing image %s (%s/%s)"%(path,col,len(im_paths))
    im = np.array(PIL.Image.open(path))
    for t in xrange(dur):
        out = out_imgs[t]
        offset = 3*h*col
        data = im[:,t,:].tostring()
        out[offset:offset+len(data)] = data

for f in out_imgs:
    f.flush()
    f.close()
