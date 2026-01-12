import pygame
import pygame_textinput
import math
import time
import csv

BG=(248,250,252)
TXT=(30,41,59)
AC=(139,92,246)
SC=(148,163,184)
CP=(255,255,255)
IP=(255,255,255,200)
GC=(226,232,240)
BC=(203,213,225)
BCL=(255,255,255)
BHL=(241,245,249)
LC=(100,116,139)

dt=False

W,H=375,812
AS=0.0001

sw,sh=W,H

p=3

pr1=[False,0]
pr2=[False,0]
pr3=[False,0]
pr4=[False,0]

p4d=[]

gx=0
gy=0
idg=False
dsx=0
dsy=0

axp=[
    [(0,0,0,0),(5,0,0,0)],
    [(0,0,0,0),(0,5,0,0)],
    [(0,0,0,0),(0,0,5,0)],
    [(0,0,0,0),(0,0,0,5)]
]

axc=[(239,68,68),(34,197,94),(59,130,246),(168,85,247)]
axn=['X','Y','Z','W']

def load_csv():
    try:
        with open('points.csv', 'r') as f:
            reader = csv.DictReader(f)
            points = []
            for row in reader:
                x = float(row['x'])
                y = float(row['y'])
                z = float(row['z'])
                w = float(row['w'])
                points.append([x, y, z, w])
            return points
    except:
        return []

def tt():
    global dt,BG,TXT,AC,SC,CP,IP,GC,BC,BCL,BHL,LC
    dt=not dt
    if dt:
        BG=(15,23,42)
        TXT=(248,250,252)
        AC=(139,92,246)
        SC=(71,85,105)
        CP=(30,41,59)
        IP=(30,41,59,200)
        GC=(51,65,85)
        BC=(71,85,105)
        BCL=(51,65,85)
        BHL=(71,85,105)
        LC=(148,163,184)
    else:
        BG=(248,250,252)
        TXT=(30,41,59)
        AC=(139,92,246)
        SC=(148,163,184)
        CP=(255,255,255)
        IP=(255,255,255,200)
        GC=(226,232,240)
        BC=(203,213,225)
        BCL=(255,255,255)
        BHL=(241,245,249)
        LC=(100,116,139)

def rxw(x,w,a):
    return x*math.cos(a)-w*math.sin(a),x*math.sin(a)+w*math.cos(a)
def ryw(y,w,a):
    return y*math.cos(a)-w*math.sin(a),y*math.sin(a)+w*math.cos(a)
def rzw(z,w,a):
    return z*math.cos(a)-w*math.sin(a),z*math.sin(a)+w*math.cos(a)
def rxy(x,y,a):
    return x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)
def rxz(x,z,a):
    return x*math.cos(a)-z*math.sin(a),x*math.sin(a)+z*math.cos(a)
def ryz(y,z,a):
    return y*math.cos(a)-z*math.sin(a),y*math.sin(a)+z*math.cos(a)

def p4_2(x,y,z,w):
    d=p/20
    x=x*d*s+W//2
    y=y*d*s+H//2
    return x,y

pygame.init()
sc=pygame.display.set_mode((W,H),pygame.RESIZABLE)
surf=pygame.Surface((W,H),pygame.SRCALPHA)
pygame.display.set_caption("4D Graph")
sw,sh=pygame.display.get_window_size()
s=100

a={'XW':0.0,'YW':0.0,'ZW':0.0,'XY':0.0,'XZ':0.45,'YZ':0.2}

kp={pygame.K_q:False,pygame.K_w:False,pygame.K_e:False,pygame.K_r:False,
    pygame.K_t:False,pygame.K_y:False,pygame.K_a:False,pygame.K_s:False,
    pygame.K_d:False,pygame.K_f:False,pygame.K_g:False,pygame.K_h:False}

f1=pygame.font.SysFont('Arial',16)
f2=pygame.font.SysFont('Arial',20)
f3=pygame.font.SysFont('Arial',14)
f4=pygame.font.SysFont('Arial',14,True)
f5=pygame.font.SysFont('Arial',18)
f6=pygame.font.SysFont('Arial',20)

ti=pygame_textinput.TextInputVisualizer(font_object=pygame.font.SysFont('Arial',20),cursor_color=AC)

rn=True
while rn:
    sc.fill(BG)
    sw,sh=pygame.display.get_window_size()
    ev=pygame.event.get()
    bn1=['XW','YW','ZW','XY','XZ','YZ','SCALE']
    bn2=['','','','','','ADD POINT','CLEAR']
    for e in ev:
        if e.type==pygame.QUIT:
            rn=False
        elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            mcp=e.pos[1]>sh*0.5454
            if not mcp:
                idg=True
                dsx=e.pos[0]
                dsy=e.pos[1]
            else:
                for i in range(7):
                    if pygame.Rect(sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.5682,sw*0.1104166,sh*0.0602).collidepoint(e.pos):
                        pr1=[True,i]
                for i in range(7):
                    if pygame.Rect(sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.6886,sw*0.1104,sh*0.0602).collidepoint(e.pos):
                        pr2=[True,i]
                for i in range(7):
                    if pygame.Rect(sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.7966,sw*0.1104,sh*0.0602).collidepoint(e.pos):
                        pr3=[True,i]
                if pygame.Rect(sw*0.0333,sh*0.9170,sw*0.775,sh*0.0602).collidepoint(e.pos):
                    pr4=[True,0]
        elif e.type==pygame.MOUSEBUTTONUP and e.button==1:
            if pr3[0] and pr3[1]==4:
                tt()
            pr1[0]=False
            pr2[0]=False
            pr3[0]=False
            pr4[0]=False
            idg=False
        elif e.type==pygame.MOUSEMOTION:
            if idg:
                gx+=e.pos[0]-dsx
                gy+=e.pos[1]-dsy
                dsx=e.pos[0]
                dsy=e.pos[1]
        elif e.type==pygame.KEYDOWN:
            if e.key in kp:
                kp[e.key]=True
        elif e.type==pygame.KEYUP:
            if e.key in kp:
                kp[e.key]=False

    if pr1[0]==True:
        if pr1[1]==6:
            p+=0.01
        else:
            a[bn1[pr1[1]]]+=AS*10
    if pr2[0]==True:
        if pr2[1]==6:
            p-=0.01
        else:
            a[bn1[pr2[1]]]-=AS*10
    if pr3[0]==True:
        if pr3[1]==5:
            if ti.value!='':
                p4d.append(list(map(float,ti.value.split())))
                ti.value=''
        elif pr3[1]==6:
            p4d = []
            time.sleep(0.2)
    if pr4[0]==True:
        if pr4[1]==0:
            loaded_points = load_csv()
            p4d.extend(loaded_points)
            time.sleep(0.2)

    rp=[]
    for x,y,z,w in p4d:
        x,w=rxw(x,w,a['XW'])
        y,w=ryw(y,w,a['YW'])
        z,w=rzw(z,w,a['ZW'])
        x,y=rxy(x,y,a['XY'])
        x,z=rxz(x,z,a['XZ'])
        y,z=ryz(y,z,a['YZ'])
        rp.append((x,y,z,w))

    pp=[]
    for x,y,z,w in rp:
        xp,yp=p4_2(x,y,z,w)
        pp.append((xp,yp))

    ra=[]
    for ax in axp:
        rax=[]
        for pt in ax:
            x,y,z,w=pt
            x,w=rxw(x,w,a['XW'])
            y,w=ryw(y,w,a['YW'])
            z,w=rzw(z,w,a['ZW'])
            x,y=rxy(x,y,a['XY'])
            x,z=rxz(x,z,a['XZ'])
            y,z=ryz(y,z,a['YZ'])
            rax.append((x,y,z,w))
        ra.append(rax)

    pa=[]
    for ax in ra:
        pax=[]
        for pt in ax:
            x,y,z,w=pt
            xp,yp=p4_2(x,y,z,w)
            pax.append((xp,yp))
        pa.append(pax)

    gs=50
    for x in range(0,sw,gs):
        pygame.draw.line(sc,GC,(x+gx%gs,0),(x+gx%gs,sh*0.5454),1)
    for y in range(0,int(sh*0.5454),gs):
        pygame.draw.line(sc,GC,(0,y+gy%gs),(sw,y+gy%gs),1)

    def ao(x,y):
        return x+gx,y+gy

    for i,ax in enumerate(pa):
        if len(ax)==2:
            x1,y1=ax[0]
            x2,y2=ax[1]
            c=axc[i]
            x1o,y1o=ao(x1+(sw/2)-185,y1+(sh/2)-590)
            x2o,y2o=ao(x2+(sw/2)-185,y2+(sh/2)-590)
            pygame.draw.line(sc,c,(x1o,y1o),(x2o,y2o),3)
            al=f3.render(axn[i],True,c)
            sc.blit(al,(x2o+8,y2o-8))

    for i in range(len(pp)-1):
        x1,y1=pp[i]
        x2,y2=pp[i+1]
        x1o,y1o=ao(x1+(sw/2)-185,y1+(sh/2)-590)
        x2o,y2o=ao(x2+(sw/2)-185,y2+(sh/2)-590)
        pygame.draw.line(sc,LC,(x1o,y1o),(x2o,y2o),2)

    for i,(xp,yp) in enumerate(pp):
        xo,yo=ao(xp+(sw/2)-185,yp+(sh/2)-590)
        pygame.draw.circle(sc,AC,(xo,yo),5)
        pygame.draw.circle(sc,BG if dt else (255,255,255),(xo,yo),3)
        try:
            q=p4d[i]
            tp=f3.render(f"P{i}: {q}",False,TXT)
            sc.blit(tp,(xo+8,yo+8))
        except:pass

    pygame.draw.line(sc,BC,(0,sh*0.5454),(sw,sh*0.5454),3)
    pygame.draw.rect(sc,CP,[0,sh*0.5454,sw,sh*0.4545])
    pygame.draw.line(sc,BC,[0,sh*0.5454],[sw,sh*0.5454],3)
    pygame.draw.rect(sc,IP,[0,0,sw*0.25,sh*0.1534])
    pygame.draw.rect(sc,BC,[0,0,sw*0.25,sh*0.1534],2)

    for i in range(7):
        bc=BHL if (pr1[0] and pr1[1]==i) else BCL
        pygame.draw.rect(sc,bc,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.5682,sw*0.1104166,sh*0.0602],border_radius=8)
        pygame.draw.rect(sc,BC,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.5682,sw*0.1104166,sh*0.0602],2,border_radius=8)
        if i==6:
            tb=f4.render(bn1[i],True,TXT)
            sc.blit(tb,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.025,sh*0.6432))
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.5982),4,1)
        else:
            tb=f4.render(bn1[i],True,TXT)
            sc.blit(tb,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.025,sh*0.6432))
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.5982),4,1)
    
    for i in range(7):
        bc=BHL if (pr2[0] and pr2[1]==i) else BCL
        pygame.draw.rect(sc,bc,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.6886,sw*0.1104,sh*0.0602],border_radius=8)
        pygame.draw.rect(sc,BC,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.6886,sw*0.1104,sh*0.0602],2,border_radius=8)
        if i==6:
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.7186),4,1)
        else:
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.7186),4,1)

    for i in range(7):
        bc=BHL if (pr3[0] and pr3[1]==i) else BCL
        pygame.draw.rect(sc,bc,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.7966,sw*0.1104,sh*0.0602],border_radius=8)
        pygame.draw.rect(sc,BC,[sw*0.0333+sw*0.0271*i+sw*0.1104*i,sh*0.7966,sw*0.1104,sh*0.0602],2,border_radius=8)
        if i==4:
            cx=sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055
            cy=sh*0.8261
            if dt:
                pygame.draw.circle(sc,AC,(cx,cy),8)
                pygame.draw.circle(sc,BCL,(cx+3,cy-3),6)
            else:
                pygame.draw.circle(sc,AC,(cx,cy),8)
                for ang in range(0,360,45):
                    ra=math.radians(ang)
                    sx=cx+10*math.cos(ra)
                    sy=cy+10*math.sin(ra)
                    ex=cx+15*math.cos(ra)
                    ey=cy+15*math.sin(ra)
                    pygame.draw.line(sc,AC,(sx,sy),(ex,ey),2)
        elif i==5:
            tb=f4.render(bn2[i],True,TXT)
            sc.blit(tb,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.025,sh*0.8705))
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.8261),4,1)
        elif i==6:
            tb=f4.render(bn2[i],True,TXT)
            sc.blit(tb,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.025,sh*0.8705))
            pygame.draw.circle(sc,AC,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.055,sh*0.8261),4,1)
        else:
            tb=f4.render(bn2[i],True,TXT)
            sc.blit(tb,(sw*0.0333+sw*0.0271*i+sw*0.1104*i+sw*0.025,sh*0.8705))

    pygame.draw.rect(sc,BHL if (pr4[0] and pr4[1]==0) else BCL,[sw*0.0333,sh*0.9170,sw*0.775,sh*0.0602],border_radius=8)
    pygame.draw.rect(sc,BC,[sw*0.0333,sh*0.9170,sw*0.775,sh*0.0602],2,border_radius=8)
    load_text = f5.render("LOAD POINTS FROM CSV", True, TXT)
    sc.blit(load_text, (sw*0.0333 + (sw*0.775 - load_text.get_width())/2, sh*0.937))

    txw=f1.render(f"XW: {a['XW']/6.3*360%360:.1f}°",False,TXT)
    txy=f1.render(f"XY: {a['XY']/6.3*360%360:.1f}°",False,TXT)
    txz=f1.render(f"XZ: {a['XZ']/6.3*360%360:.1f}°",False,TXT)
    tyw=f1.render(f"YW: {a['YW']/6.3*360%360:.1f}°",False,TXT)
    tyz=f1.render(f"YZ: {a['YZ']/6.3*360%360:.1f}°",False,TXT)
    tzw=f1.render(f"ZW: {a['ZW']/6.3*360%360:.1f}°",False,TXT)

    sc.blit(txw,(sw*0.02,sh*0.015))
    sc.blit(tyw,(sw*0.02,sh*0.038))
    sc.blit(tzw,(sw*0.02,sh*0.061))
    sc.blit(txz,(sw*0.02,sh*0.084))
    sc.blit(tyz,(sw*0.02,sh*0.107))
    sc.blit(txy,(sw*0.02,sh*0.130))
    
    lt=f3.render("Axes:",True,TXT)
    sc.blit(lt,(sw*0.15,sh*0.015))
    
    ly=sh*0.04
    for i,(c,n) in enumerate(zip(axc,axn)):
        pygame.draw.line(sc,c,(sw*0.15,ly+i*16),(sw*0.18,ly+i*16),3)
        al=f3.render(f"{n}-axis",True,c)
        sc.blit(al,(sw*0.19,ly+i*16-6))
    
    il=f3.render("Add point (x y z w):",True,TXT)
    sc.blit(il,(sw-180,15))
    
    pygame.draw.rect(sc,BG,[sw-170,40,160,35],border_radius=6)
    pygame.draw.rect(sc,AC,[sw-170,40,160,35],2,border_radius=6)
    
    ti.update(ev)
    sc.blit(ti.surface,(sw-165,45))

    sc.blit(surf,(0,0))

    pygame.display.flip()

pygame.quit()
