# cut a dish on a plain studio backdrop as an ellipse fitted to its non-background pixels (no colour-keying of the dish itself)
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
src,out=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(int)
bgc=np.median(np.concatenate([a[:20].reshape(-1,3),a[-20:].reshape(-1,3),a[:,:20].reshape(-1,3),a[:,-20:].reshape(-1,3)]),0)
d=np.abs(a-bgc).sum(2)>14
d=ndimage.binary_opening(d,iterations=3); lab,n=ndimage.label(d); big=np.argmax(ndimage.sum(d,lab,range(1,n+1)))+1
ys,xs=np.where(ndimage.binary_fill_holes(lab==big))
x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max(); print('bbox',x0,y0,x1,y1,im.size)
m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse([x0,y0,x1,y1],fill=255)
m=m.resize((im.width*2,im.height*2)).filter(ImageFilter.GaussianBlur(1.5)).resize(im.size,Image.LANCZOS)
rgba=im.convert('RGBA'); rgba.putalpha(m); rgba.crop((x0,y0,x1+1,y1+1)).save(out)
