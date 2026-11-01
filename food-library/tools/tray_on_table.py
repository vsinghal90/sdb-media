# Usage: python3 tray_on_table.py <meal> <out.jpg>  -- puts a food-library tray on photos/table.jpg with contact + soft shadow
import sys
from PIL import Image, ImageFilter, ImageEnhance
meal,out=sys.argv[1],sys.argv[2]
bg=Image.open('photos/table.jpg').convert('RGB')
tr=Image.open('/mnt/project-files/food-library/meals/tray/%s.png'%meal).convert('RGBA')
W=900; tr=tr.resize((W,int(tr.height*W/tr.width)),Image.LANCZOS)
# warm the tray slightly to match afternoon window light
rgb=ImageEnhance.Brightness(tr.convert('RGB')).enhance(0.98); r,g,b=rgb.split()
r=r.point(lambda v:min(255,int(v*1.03))); b=b.point(lambda v:int(v*0.95))
tr=Image.merge('RGBA',(r,g,b,tr.split()[3]))
x=(1080-W)//2; y=1160-tr.height//2
a=tr.split()[3]
def shadow(off,blur,op):
    s=Image.new('L',bg.size,0); s.paste(a,(x+off[0],y+off[1])); s=s.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*op))
    return s
dark=Image.new('RGB',bg.size,(30,16,6))
bg=Image.composite(dark,bg,shadow((26,30),28,0.45))
bg=Image.composite(dark,bg,shadow((4,6),6,0.6))
bg.paste(tr,(x,y),tr)
bg.save(out,quality=93); print(out,x,y,tr.size)
