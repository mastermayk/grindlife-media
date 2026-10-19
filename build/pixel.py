# Pixel-art generator for Grind Life RPG X assets (Save Point direction).
# Sprites + palette ported from design/directions/2-save-point/pixel.js / scene.js.
from PIL import Image, ImageDraw
PAL={'K':'#1E1530','W':'#FFF5DA','S':'#8D5A3B','s':'#6B4129','C':'#FF4F6A','c':'#C9324D','T':'#3ED6C4','t':'#23A194','G':'#FFC23D','g':'#C98A12',
 'P':'#8B5CF6','p':'#6237C9','B':'#C4B0FF','Y':'#FFE45C','R':'#FF4F6A','O':'#FF8A3D','M':'#3ED6C4','V':'#8B5CF6','H':'#1E1530','D':'#2A2150','L':'#7BD34A','l':'#4E9A2A'}
SPR={
'hero':["......KKKK......","....KKCCCCKK....","...KCCCCCCCcK...","..KCCCCCCCCCcK..","..KKKKKKKKKKKKKK","..KHSSSSSSSSHK..","..KSSSSSSSSSSK..","..KSKKSSSSKKSK..","..KSSSSSSSSSsK..","...KSSSKKSSsK...","....KKSSSSKK....","...KKTTGGTTKK...","..KTTTTGGTTTTK..",".KTTTTTTTTTTttK.",".KTTKTTTTTTKTtK.",".KSKTTTTTTTTKSK.",".KSKTTTttTTTKSK.","..KKTTTTTTTTKK..","...KDDDDDDDDK...","...KDDDKKDDDK...","...KDDDKKDDDK...","...KDDK..KDDK...","..KWWWK..KWWWK..","..KKKKK..KKKKK.."],
'heart':[".KK...KK.","KRRK.KRRK","KRWRKRRRK","KRRRRRRRK",".KRRRRRK.","..KRRRK..","...KRK...","....K...."],
'coin':["..KKKK..",".KGGGGK.","KGGWGGgK","KGWGGGgK","KGGGGGgK","KGGGGggK",".KggggK.","..KKKK.."],
'flame':["...K....","..KOK...","..KOOK..",".KOOYOK.",".KOYYOK.","KOYYYYOK","KOYWWYOK",".KOYYOK.","..KKKK.."],
'sword':[".......KK","......KWK",".....KWK.","....KWK..","K..KWK...",".KKWK....","..KK.....",".KGKK....","KK..K...."],
}
def spr(img,name,x0,y0,s=1):
    d=ImageDraw.Draw(img)
    for y,row in enumerate(SPR[name]):
        for x,ch in enumerate(row):
            if ch!='.' and ch in PAL: d.rectangle([x0+x*s,y0+y*s,x0+x*s+s-1,y0+y*s+s-1],fill=PAL[ch])
class LCG:
    def __init__(s,seed): s.v=seed
    def __call__(s): s.v=(s.v*16807)%2147483647; return s.v/2147483647
def scene(W,H,ground,seed=7,moon=None,tower=None,tank=None,stars=26,star_h=None,back=(10,24),front=(8,12),moon_r=1):
    img=Image.new('RGB',(W,H),'#17122B'); d=ImageDraw.Draw(img)
    R=lambda x,y,w,h,c: d.rectangle([x,y,x+w-1,y+h-1],fill=c) if w>0 and h>0 else None
    rnd=LCG(seed)
    bands=['#17122B','#1d1636','#241b45','#2e2257','#3b2a66']
    bh=max(1,round(ground*0.16))
    for i,c in enumerate(bands): R(0,i*bh,W,bh+1,c)
    for i in range(4):
        for x in range(i%2,W,2): R(x,(i+1)*bh,1,1,bands[i])
    R(0,5*bh,W,H-5*bh,'#3b2a66')
    sh=star_h or int(ground*0.5)
    for i in range(stars):
        x=int(rnd()*W); y=int(rnd()*sh); R(x,y,1,1,'#FFC23D' if rnd()>.7 else '#B9A9F0')
    if moon:
        mx,my=moon; n=9*moon_r
        for y in range(n):
            for x in range(n):
                X,Y=x/moon_r,y/moon_r
                if (X-4)**2+(Y-4)**2<=17 and (X-6)**2+(Y-3)**2>11: R(mx+x,my+y,1,1,'#FFE9A8')
    base=ground+6  # scene.js: buildings anchored to the 50-row bottom; ground at 44
    x=0
    while x<W:
        w=4+int(rnd()*7); h=back[0]+int(rnd()*back[1]); R(x,base-h-8,w,h+8,'#3a2c6e'); x+=w
    if tower:
        tx,th=tower; top=base-th
        R(tx,top,7,th,'#2c2160'); R(tx+3,top-5,1,5,'#2c2160'); R(tx+3,top-6,1,1,'#FF4F6A')
        for y in range(top+3,ground+2,3):
            for xx in range(tx+1,tx+6,2):
                if rnd()>.45: R(xx,y,1,1,'#FFC23D')
    x=-2
    while x<W:
        w=6+int(rnd()*9); h=front[0]+int(rnd()*front[1]); top=base-h-6; R(x,top,w,h+6,'#21194a')
        for yy in range(top+2,base,3):
            for xx in range(x+1,x+w-1,2):
                if rnd()>.62: R(xx,yy,1,1,'#FFC23D' if rnd()>.3 else '#3ED6C4')
        x+=w+(1 if rnd()>.6 else 0)
    R(0,ground,W,H-ground,'#120d24'); R(0,ground-1,W,1,'#4b3a85')
    for xx in range(0,W,6): R(xx,ground+1,1,H-ground-1,'#1d1638')
    if tank:
        tx=tank; ty=ground-10
        R(tx,ty,10,7,'#120d24');R(tx+1,ty+1,8,1,'#4b3a85');R(tx+1,ty+7,1,2,'#120d24');R(tx+8,ty+7,1,2,'#120d24')
        R(tx+16,ground-14,1,13,'#120d24');R(tx+14,ground-14,5,1,'#120d24')
    return img
def up(img,k): return img.resize((img.width*k,img.height*k),Image.NEAREST)
def outline_spr(img,name,x0,y0,s,col='#6a56a8',t=1):
    # pixel outline (t logical px) around the sprite silhouette so it pops off dark buildings
    rows=SPR[name]; d=ImageDraw.Draw(img); filled=set()
    for y,row in enumerate(rows):
        for x,ch in enumerate(row):
            if ch!='.':
                for yy in range(y0+y*s,y0+y*s+s):
                    for xx in range(x0+x*s,x0+x*s+s): filled.add((xx,yy))
    ring=set()
    for (x,y) in filled:
        for dx in range(-t,t+1):
            for dy in range(-t,t+1):
                p=(x+dx,y+dy)
                if p not in filled: ring.add(p)
    for p in ring: d.point(p,fill=col)
