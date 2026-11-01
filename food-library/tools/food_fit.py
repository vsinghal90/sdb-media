# Check that every food item stays whole inside the 1080x1920 frame at the scene's largest zoom.
# Usage: python3 food_fit.py placements.json
# placements.json: [{"scene":"bisi","box":[x0,y0,x1,y1],"zoom":1.04,"origin":[540,960],"margin":24}, ...]
#   box = the dish (or tray) bounding box in the 1080x1920 scene image, from the alpha bbox when it was placed
#   zoom = the largest CSS scale the scene reaches (push/pan animations); origin = transform origin (default centre)
import json, sys
W,H=1080,1920; bad=0
for p in json.load(open(sys.argv[1])):
    z=p.get('zoom',1.0); ox,oy=p.get('origin',[W/2,H/2]); m=p.get('margin',24)
    x0,y0,x1,y1=p['box']; X0,Y0,X1,Y1=ox+(x0-ox)*z,oy+(y0-oy)*z,ox+(x1-ox)*z,oy+(y1-oy)*z
    ok=X0>=m and Y0>=m and X1<=W-m and Y1<=H-m
    bad+=not ok
    print(('OK  ' if ok else 'CUT '),p['scene'],'at zoom',z,'->',[round(v) for v in (X0,Y0,X1,Y1)])
sys.exit(1 if bad else 0)
