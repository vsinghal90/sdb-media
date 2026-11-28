# Usage: python3 tray_persp.py <scene.jpg> <meal-or-png> <out.jpg> [width] [bottom_y]
# Lays a top-down food-library tray onto an eye-level table with a perspective squash, contact + soft shadow.
import sys, numpy as np
from PIL import Image, ImageFilter
scene,src,out=sys.argv[1:4]; W=int(sys.argv[4]) if len(sys.argv)>4 else 860; BY=int(sys.argv[5]) if len(sys.argv)>5 else 1830
bg=Image.open(scene).convert('RGB')
p=src if src.endswith(('.png','.webp')) else '/mnt/project-files/food-library/meals/tray/%s.png'%src
tr=Image.open(p).convert('RGBA'); tr=tr.crop(tr.split()[3].getbbox())
tr=tr.resize((W,int(tr.height*W/tr.width)),Image.LANCZOS)
w,h=tr.size; H=int(h*0.5); top_inset=int(w*0.08)
# perspective: map output quad (top narrower) back to source rect
def coeffs(pa,pb):
    A=[];B=[]
    for (x,y),(X,Y) in zip(pa,pb):
        A.append([x,y,1,0,0,0,-X*x,-X*y]);A.append([0,0,0,x,y,1,-Y*x,-Y*y]);B+= [X,Y]
    return np.linalg.solve(np.array(A,float),np.array(B,float))
dst=[(top_inset,0),(w-top_inset,0),(w,H),(0,H)]; srcq=[(0,0),(w,0),(w,h),(0,h)]
pt=tr.transform((w,H),Image.PERSPECTIVE,coeffs(dst,srcq),Image.BICUBIC)
x=(1080-w)//2; y=BY-H
a=pt.split()[3]; dark=Image.new('RGB',bg.size,(25,14,6))
for off,bl,op in [((0,14),18,.55),((0,4),5,.7)]:
    s=Image.new('L',bg.size,0); s.paste(a,(x+off[0],y+off[1])); s=s.filter(ImageFilter.GaussianBlur(bl)).point(lambda v:int(v*op)); bg=Image.composite(dark,bg,s)
bg.paste(pt,(x,y),pt); bg.save(out,quality=93); print(out,(x,y,w,H))
