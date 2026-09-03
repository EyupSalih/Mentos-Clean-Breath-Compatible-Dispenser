import cadquery as cq, math
from cadquery import importers
P='/mnt/data/Mentos_CleanBreath_V7_FUNCTIONAL_CAD/STEP_parts/'
load=lambda n: importers.importStep(P+n)
ch=load('01_lower_chassis_closed_shell.step');tb=load('02_transfer_base_metering_deck.step');tc=load('03_top_cap_real_screw_access.step');mag=load('04_magazine_LEFT_double_J.step');fol=load('06_follower_double_stem_PRINT_2.step');sh=load('08_dual_pocket_CUTOFF_shuttle.step');bar=load('09_internal_common_release_bar.step');cap=load('12_full_sliding_bottom_outer_cover.step')
# params exact
xL,xR=-9.5,9.5; mag_y=-1.35; mag_bottom_z=3.2; follower_t=2.35; lock_center=12.4; lock_angle=18; release_z=12.6;release_y=10.0;release_travel=2.45
feed_ring_bottom=3.2+(107.8-3.2-0.90);feed_ring_top=feed_ring_bottom+0.78; top_bottom=feed_ring_top+0.06; tcenter=top_bottom+5.9/2;tcentermax=top_bottom+6.2/2;second_top=feed_ring_bottom-0.08;second_center=second_top-5.9/2
sh_bottom=feed_ring_top+0.20; shift=9.5; pocketdx=9.5; tablet_d=11.2;tablet_t=5.9; dmax=11.55;tmax=6.2

def tx(o,x=0,y=0,z=0):return o.translate((x,y,z))
def rz(o,a):return o.rotate((0,0,0),(0,0,1),a)
def iv(a,b):
    try:return float(a.val().intersect(b.val()).Volume())
    except:return float('nan')
def tablet(c,d=tablet_d,t=tablet_t):
    x,y,z=c;o=cq.Workplane('XY').circle(d/2).extrude(t)
    try:o=o.edges().fillet(min(.72,t/3))
    except:pass
    return o.translate((x,y,z-t/2))
magL=tx(mag,xL,mag_y,mag_bottom_z);magR=tx(mag,xR,mag_y,mag_bottom_z)
def follower(side,z,a=0):return tx(rz(fol,a),xL if side=='L' else xR,mag_y,z-follower_t/2)
def shuttle(sx):return tx(sh,sx,mag_y,sh_bottom)
def rel(dx):return tx(bar,dx,release_y,release_z)
print('release rigid sweeps')
for dx in [0,.5,1,1.5,2,2.5,3.15]: print(dx,iv(rel(dx),ch),iv(rel(dx),magL),iv(rel(dx),magR))
print('release contacts')
for side in ['L','R']: print(side,iv(rel(release_travel),follower(side,lock_center,lock_angle)),iv(rel(0),follower(side,lock_center,lock_angle)))
print('shuttle + candy sweep selected')
for sx in [-9.5,-7.125,-4.75,-2.375,0,2.375,4.75,7.125,9.5]:
 s=shuttle(sx); print('s',sx,'rigid',iv(s,tb),iv(s,tc),iv(s,ch))
 for px in [-9.5,9.5]:
  t=tablet((px+sx,mag_y,tcenter));tm=tablet((px+sx,mag_y,tcentermax),dmax,tmax)
  print(' carry',px,'nom',sum(iv(t,o) for o in [tb,tc,ch,s]),'max',sum(iv(tm,o) for o in [tb,tc,ch,s]))
 for xc in [xL,xR]:
  nt=tablet((xc,mag_y,second_center));print(' next',xc,iv(nt,s))
print('blocking')
for sx in [-9.5,9.5]:
 s=shuttle(sx)
 for xc in [xL,xR]:
  probe=tablet((xc,mag_y,tcenter-.8),dmax,tmax);print(sx,xc,iv(probe,s))
print('neutral max')
s=shuttle(0)
for xc in [xL,xR]: print(xc,iv(tablet((xc,mag_y,tcentermax),dmax,tmax),s))
print('exit')
for sx in [-9.5,9.5]:
 s=shuttle(sx)
 for dy in [0,-2,-4,-6,-8,-10,-12,-14]:
  t=tablet((0,mag_y+dy,tcenter));tm=tablet((0,mag_y+dy,tcentermax),dmax,tmax)
  print(sx,dy,sum(iv(t,o) for o in [tb,tc,ch,s]),sum(iv(tm,o) for o in [tb,tc,ch,s]))
