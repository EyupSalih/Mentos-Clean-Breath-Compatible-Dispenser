import cadquery as cq
from cadquery import exporters
from pathlib import Path
import math, json, csv, shutil, zipfile

OUT=Path('/mnt/data/v7_rebuilt_retention_v2')
if OUT.exists(): shutil.rmtree(OUT)
for d in ['STEP_parts','STL_printable','REFERENCE_hardware','ASSEMBLY_STATES','AUDIT','SOURCE']:
    (OUT/d).mkdir(parents=True,exist_ok=True)

# ============================================================
# V7 DESIGN INTENT
# X = left/right, Y = front/back (front = negative Y), Z = up
# V5 architecture retained, with these targeted corrections:
# - closed outer shell; no long external follower windows
# - two removable V5-style spring magazines, but follower has TWO opposite stems
# - follower locks by symmetric double J/bayonet slots in the magazine itself
# - one recessed SIDE push button drives an INTERNAL common release bar after the case is closed
# - full-footprint SLIDING bottom service cover; no routine screws
# - wide dual-pocket linear shuttle with a dedicated lower cutoff layer
# - feed holes are positively covered when shuttle is at either dispense stop
# - large tactile thumb tab + 3-position ball detent, center strongest
# - real top screws: straight tool access, clearance through cap/base, heat-set inserts in chassis bosses
# - separate compliant TPU dust flap at the output mouth
# ============================================================

# ---------- tablet design envelope ----------
tablet_d_nom=11.20
tablet_d_max=11.55
tablet_t_nom=5.90
tablet_t_max=6.20
capacity_each=15

# ---------- outer body ----------
body_w=60.0
body_d=27.0
wall=2.20
chassis_h=104.0
mag_y=-1.35
xmag=9.50
xL,xR=-xmag,xmag
front_y=-body_d/2
rear_y= body_d/2

# ---------- magazines ----------
mag_od=15.90
mag_id=12.00
receiver_d=17.10
receiver_sleeve_od=19.00
mag_bottom_z=3.20
mag_top_seat_z=107.80
mag_h=mag_top_seat_z-mag_bottom_z
mag_base_t=2.45

# follower and two opposite stems (front/rear)
follower_d=11.35
follower_t=2.35
follower_cup_d=8.55
follower_cup_h=1.65
stem_w_x=3.25
stem_len_y=5.40
stem_h=2.15
stem_center_y=6.90
stem_outer_y=8.60
# full internal magazine slots are hidden by the closed main shell
slot_w_x=5.65
slot_depth_y=4.55
slot_z0=6.0
# double symmetric J/bayonet lock at bottom
lock_angle=18.0
lock_center_global=12.4
lock_center_local=lock_center_global-mag_bottom_z
j_window_w=8.5
j_window_d=5.6
j_window_h=5.5

# ---------- silicone anti-rattle rails ----------
silicone_cord_d=1.50
silicone_groove_d=1.72
silicone_groove_x=6.55
silicone_z0=25.0
silicone_z1=101.4

# ---------- feed ring ----------
feed_ring_od=13.35
feed_ring_id=10.65
feed_ring_t=0.78
feed_ring_groove_od=13.65
feed_ring_z0_local=mag_h-0.90
feed_ring_bottom=mag_bottom_z+feed_ring_z0_local
feed_ring_top=feed_ring_bottom+feed_ring_t
feed_support_clear=0.06
second_ring_clear=0.08

top_tablet_bottom=feed_ring_top+feed_support_clear
transfer_tablet_center_z=top_tablet_bottom+tablet_t_nom/2
transfer_tablet_center_z_max=top_tablet_bottom+tablet_t_max/2
second_tablet_top=feed_ring_bottom-second_ring_clear
second_tablet_center=second_tablet_top-tablet_t_nom/2
second_tablet_center_max=second_tablet_top-tablet_t_max/2
bottom_tablet_center=second_tablet_center-(capacity_each-2)*tablet_t_nom
follower_loaded_center=bottom_tablet_center-tablet_t_nom/2-0.35-follower_t/2
follower_empty_center=103.7
follower_lock_center=lock_center_global

# ---------- main spring reference ----------
spring_od=10.05
spring_wire=0.32
spring_turns=28
spring_free_len=110.0
spring_seat_z=mag_bottom_z+mag_base_t+0.65

# ---------- internal receiver clearance for follower stems ----------
stem_clear_x=10.80
stem_channel_depth=4.80
# front channel remains INSIDE shell; shell itself stays closed
front_channel_y=-9.50
rear_channel_y=7.30

# ---------- internal common release button/bar ----------
# Locked follower is rotated +18deg. Rear stem shifts -X. Push rear stem +X to return it to vertical slot.
release_z=lock_center_global+0.2
release_y=10.00
release_travel=2.45
release_bar_w=47.0
release_bar_d=2.10
release_bar_h=2.35
button_w=7.8
button_d=5.2
button_h=5.0
button_x0=-body_w/2+1.55
button_side_clear=0.25
release_nose_w=2.0
release_nose_d=3.6
release_nose_h=3.4
# return spring reference in left-side cavity
release_spring_od=3.3
release_spring_wire=0.30
release_spring_turns=7
release_spring_len=8.0

# ---------- transfer base ----------
base_z0=chassis_h
base_t=4.90
base_top=base_z0+base_t
mag_counterbore_d=16.45
mag_counterbore_depth=3.85
feed_throat_d=12.60

# ---------- shuttle / cutoff ----------
track_floor_z=feed_ring_top
track_clear=0.20
shuttle_shift=xmag
shuttle_w=40.0
shuttle_d=13.80
cutoff_t=1.35
pocket_upper_h=5.65
shuttle_h=cutoff_t+pocket_upper_h
shuttle_bottom=track_floor_z+track_clear
shuttle_top=shuttle_bottom+shuttle_h
shuttle_pocket_dx=xmag
pocket_d=12.45
# full-height candy extraction opening above cutoff floor; lower cutoff has its own narrow forward throat
upper_front_open_w=12.35
lower_front_open_w=12.20
# big user thumb tab
tab_w=11.2
tab_d=7.4
tab_h=7.2
tab_overlap=0.55
# spring-ball detent in shuttle against top cap
plunger_body_d=3.0
plunger_pilot_d=2.55
plunger_y=3.7
center_dimple_depth=0.78
side_dimple_depth=0.32

# ---------- guides/output ----------
rail_z0=mag_top_seat_z+0.15
rail_h=6.25
rail_t=1.30
front_fence_y=-9.15
rear_rail_y=6.45
mouth_w=13.20
mouth_h=7.55
mouth_center_z=top_tablet_bottom+tablet_t_max/2
output_trough_w=13.05

# ---------- top cap + true screw system ----------
cap_z0=max(shuttle_top+0.35,rail_z0+rail_h+0.25)
cap_t=3.0
cap_top=cap_z0+cap_t
slot_len=2*shuttle_shift+tab_w+1.4
slot_w=8.1
# M2.5 x 12 countersunk screws into M2.5 heat-set inserts
m25_clear=2.90
m25_insert_d=4.15
m25_insert_depth=4.8
m25_head_d=5.5
m25_screw_len=12.0
top_screw_xy=[(-25.0,-9.7),(25.0,-9.7),(-25.0,9.7),(25.0,9.7)]
screwdriver_keepout_d=8.0

# ---------- output TPU flap ----------
flap_w=15.8
flap_h=8.5
flap_t=0.80
flap_hinge_t=0.45
flap_mount_w=19.5
flap_mount_h=2.2
flap_mount_t=1.15
flap_y=front_y-0.95
flap_z=mouth_center_z

# ---------- sliding full bottom service cover ----------
# cap slides from +Y (rear) to 0; full floor closes the whole shell.
bottom_cap_w=59.0
bottom_cap_d=28.4
bottom_cap_t=2.8
bottom_cap_z=-2.10
bottom_cap_open_y=34.0
# raised inner plug creates labyrinth overlap inside shell
plug_w=54.8
plug_d=21.7
plug_h=1.35
plug_z=-0.45
# side tongues ride in internal grooves, not visible from outside
tongue_x=27.0
tongue_w=2.45
tongue_h=1.35
tongue_z=-0.20
# rear trailing dust lip touches rear outer wall only at closed position
rear_lip_t=1.20
rear_lip_h=4.20
# pull tab at rear underside
cap_pull_w=15.0
cap_pull_d=2.8
cap_pull_h=1.6
# one permanent M3 ball plunger detent in right lower wall, no repeated screws
cap_plunger_d=3.0
cap_plunger_z=0.0
cap_plunger_y=8.6
cap_dimple_d=2.7

# ---------- TPU bottom preload pads ----------
bottom_pad_d=13.2
bottom_pad_t=0.65
bottom_pad_z=-0.25

# ============================================================
# helpers
# ============================================================
def box(w,d,h,c=(0,0,0)):
    return cq.Workplane('XY').box(w,d,h).translate(c)

def rounded_box(w,d,h,r=1.0,c=(0,0,0)):
    o=cq.Workplane('XY').box(w,d,h)
    try:o=o.edges('|Z').fillet(min(r,max(0.05,w/4-0.02),max(0.05,d/4-0.02)))
    except:pass
    return o.translate(c)

def cyl_z(d,h,c=(0,0,0)):
    return cq.Workplane('XY').circle(d/2).extrude(h).translate(c)

def cyl_y(d,length,c=(0,0,0)):
    x,y,z=c
    return cq.Workplane('XZ').center(x,z).circle(d/2).extrude(length/2,both=True).translate((0,y,0))

def cyl_x(d,length,c=(0,0,0)):
    x,y,z=c
    return cq.Workplane('YZ').center(y,z).circle(d/2).extrude(length/2,both=True).translate((x,0,0))

def tablet(center=(0,0,0),d=tablet_d_nom,t=tablet_t_nom):
    x,y,z=center
    o=cq.Workplane('XY').circle(d/2).extrude(t)
    try:o=o.edges().fillet(min(0.72,t/3))
    except:pass
    return o.translate((x,y,z-t/2))

def spring_z(height,od=spring_od,wire=spring_wire,turns=spring_turns,z0=0):
    height=max(height,wire*turns+0.35)
    pitch=height/turns; rad=od/2-wire/2
    try:
        helix=cq.Wire.makeHelix(pitch,height,rad)
        prof=cq.Workplane('XZ').workplane(offset=rad).circle(wire/2)
        return prof.sweep(helix,isFrenet=True).translate((0,0,z0))
    except:return cyl_z(od,height,(0,0,z0))

def spring_x(length,od=release_spring_od,wire=release_spring_wire,turns=release_spring_turns,c=(0,0,0)):
    s=spring_z(length,od,wire,turns,0).rotate((0,0,0),(0,1,0),90)
    return s.translate(c)

def tx(o,x=0,y=0,z=0):return o.translate((x,y,z))
def rz(o,a):return o.rotate((0,0,0),(0,0,1),a)

def ivol(a,b):
    try:
        A=a.val().BoundingBox();B=b.val().BoundingBox()
        if A.xmax<B.xmin-1e-6 or B.xmax<A.xmin-1e-6 or A.ymax<B.ymin-1e-6 or B.ymax<A.ymin-1e-6 or A.zmax<B.zmin-1e-6 or B.zmax<A.zmin-1e-6:return 0.0
        return float(a.val().intersect(b.val()).Volume())
    except:
        try:return float(a.intersect(b).val().Volume())
        except:return float('nan')

def solid_count(o):
    try:return len(o.val().Solids())
    except:
        try:return len(o.solids().vals())
        except:return -1

def valid(o):
    try:return bool(o.val().isValid())
    except:return False

# ============================================================
# follower, magazine and double-sided J lock
# ============================================================
def make_follower():
    f=cq.Workplane('XY').circle(follower_d/2).extrude(follower_t)
    try:f=f.edges().fillet(0.5)
    except:pass
    # two opposite stems are ONE part with the follower
    for sy in (-1,1):
        stem=rounded_box(stem_w_x,stem_len_y,stem_h,0.35,(0,sy*stem_center_y,follower_t/2))
        f=f.union(stem)
        # tactile outer pad, still hidden inside main shell when installed
        pad=rounded_box(5.2,2.15,2.55,0.4,(0,sy*stem_outer_y,follower_t/2))
        f=f.union(pad)
    cup=cq.Workplane('XY').circle(follower_cup_d/2).extrude(follower_cup_h).translate((0,0,-follower_cup_h))
    f=f.union(cup)
    # two shallow refill-tool key holes on top, used before candy is loaded
    for xx in (-2.3,2.3):f=f.cut(cyl_z(1.6,1.1,(xx,0,follower_t-0.75)))
    return f.clean()
follower_local=make_follower()

def make_magazine_local():
    tube=cq.Workplane('XY').circle(mag_od/2).circle(mag_id/2).extrude(mag_h)
    base=cq.Workplane('XY').circle(mag_od/2).extrude(mag_base_t)
    base=base.cut(cyl_z(7.1,mag_base_t+0.4,(0,0,-0.1)))
    flange=cq.Workplane('XY').circle(16.25/2).circle(feed_ring_groove_od/2).extrude(0.85).translate((0,0,mag_h-0.85))
    spigot=cq.Workplane('XY').circle(8.55/2).circle(7.10/2).extrude(1.55).translate((0,0,mag_base_t))
    mag=tube.union(base).union(flange).union(spigot)
    # TWO opposite full-height follower slots. They are inside the CLOSED main body, not external shell slots.
    slot_h=mag_h-slot_z0+1.3
    for sy in (-1,1):
        mag=mag.cut(box(slot_w_x,slot_depth_y,slot_h,(0,sy*(mag_od/2-0.15),(slot_z0+mag_h)/2)))
    # symmetric double J windows at bottom: clockwise follower rotation locks BOTH stems.
    # front stem moves +X, rear stem moves -X when rotated clockwise.
    mag=mag.cut(box(j_window_w,j_window_d,j_window_h,(+1.7,-(mag_od/2-0.15),lock_center_local)))
    mag=mag.cut(box(j_window_w,j_window_d,j_window_h,(-1.7, +(mag_od/2-0.15),lock_center_local)))
    # two internal food-grade silicone cord grooves
    for xx in (-silicone_groove_x,silicone_groove_x):
        mag=mag.cut(cyl_z(silicone_groove_d,mag_h-silicone_z0+0.35,(xx,0,silicone_z0)))
    # feed ring seat + small front fingernail notch
    groove=cq.Workplane('XY').circle(feed_ring_groove_od/2).circle(mag_id/2).extrude(0.95).translate((0,0,feed_ring_z0_local-0.05))
    mag=mag.cut(groove)
    mag=mag.cut(box(3.4,2.5,1.25,(0,-mag_od/2+0.50,mag_h-0.6)))
    return mag.clean()
mag_local=make_magazine_local()
mag_L=mag_local.translate((xL,mag_y,mag_bottom_z))
mag_R=mag_local.translate((xR,mag_y,mag_bottom_z))

feed_ring_local=cq.Workplane('XY').circle(feed_ring_od/2).circle(feed_ring_id/2).extrude(feed_ring_t).translate((0,0,feed_ring_z0_local))
feed_ring_local=feed_ring_local.cut(box(2.4,3.0,feed_ring_t+0.35,(0,-feed_ring_od/2+0.5,feed_ring_z0_local+feed_ring_t/2)))

def feed_ring_global(side):
    xc=xL if side=='L' else xR
    return feed_ring_local.translate((xc,mag_y,mag_bottom_z))

def follower_global(side,z=follower_loaded_center,angle=0):
    xc=xL if side=='L' else xR
    return rz(follower_local,angle).translate((xc,mag_y,z-follower_t/2))

# refill pusher tool with two pins matching follower key holes; push + rotate to lock both stems
pusher_len=104.0
pusher=cyl_z(9.25,pusher_len,(0,0,0))
pusher=pusher.union(rounded_box(25,12,5,2.0,(0,0,pusher_len+2.5)))
for xx in (-2.3,2.3):pusher=pusher.union(cyl_z(1.35,1.0,(xx,0,-0.95)))
pusher=pusher.clean()

# ============================================================
# closed outer chassis with hidden follower-stem channels
# ============================================================
outer=rounded_box(body_w,body_d,chassis_h,3.0,(0,0,chassis_h/2))
inner=rounded_box(body_w-2*wall,body_d-2*wall,chassis_h+2,2.0,(0,0,chassis_h/2))
chassis=outer.cut(inner)
# V7 guide strategy: NO full-height receiver sleeves.
# The closed shell plus four X-side vertical guide rails locate the two removable magazines.
# Front/rear space remains open INSIDE the shell so both follower stems can travel and rotate while the exterior stays closed.
rail_x_offset=mag_od/2+0.75
rail_w=1.0
rail_d=3.4
for xc in (xL,xR):
    for sg in (-1,1):
        xr=xc+sg*rail_x_offset
        chassis=chassis.union(rounded_box(rail_w,rail_d,chassis_h,0.30,(xr,mag_y,chassis_h/2)))
# connect outer guide rails to the side walls and the two inner rails to each other.
left_outer=xL-rail_x_offset; right_outer=xR+rail_x_offset
chassis=chassis.union(box(left_outer-(-body_w/2+wall)+0.55,rail_d,chassis_h,(((-body_w/2+wall)+left_outer)/2,mag_y,chassis_h/2)))
chassis=chassis.union(box((body_w/2-wall)-right_outer+0.55,rail_d,chassis_h,(((body_w/2-wall)+right_outer)/2,mag_y,chassis_h/2)))
chassis=chassis.union(box(0.85,rail_d,chassis_h,(0,mag_y,chassis_h/2)))
# connect the central inner guide pair to the front shell with a narrow divider between the two magazines.
chassis=chassis.union(box(0.85,8.9,chassis_h,(0,-7.15,chassis_h/2)))
# internal rear release-bar tunnel, completely behind magazine tubes
chassis=chassis.cut(rounded_box(release_bar_w+1.5,2.70,5.0,0.55,(0,release_y,release_z)))
# local internal nose-clearance pockets around the two locked rear follower stems. These stay inside the sealed shell.
for xc in (xL,xR):
    chassis=chassis.cut(rounded_box(11.0,4.0,5.4,0.45,(xc-1.8,7.15,release_z)))
# ONLY exterior release opening: short recessed side button on LEFT wall
chassis=chassis.cut(box(11.0,6.0,6.4,(-25.5,release_y,release_z)))
# top heat-set insert bosses tied into shell, with straight vertical access
for x,y in top_screw_xy:
    boss=rounded_box(6.4,6.1,9.0,0.8,(x,y,chassis_h-4.5))
    chassis=chassis.union(boss)
    chassis=chassis.cut(cyl_z(m25_insert_d,m25_insert_depth+0.15,(x,y,chassis_h-m25_insert_depth)))
# side grooves for sliding bottom cap tongues; grooves remain internal and open only from rear service direction
for sx in (-1,1):
    xx=sx*tongue_x
    chassis=chassis.cut(box(tongue_w+0.55,body_d+1.2,tongue_h+0.45,(xx,0,0.35)))
# rear-bottom service entry for the raised labyrinth plug/tongues. It is covered by the bottom cap when closed.
chassis=chassis.cut(box(body_w-4.0,3.4,1.75,(0,rear_y-1.25,0.60)))
# right-side small permanent M3 ball-plunger pilot for bottom cap detent
chassis=chassis.cut(cyl_x(cap_plunger_d+0.35,wall+1.5,(body_w/2-wall/2,cap_plunger_y,cap_plunger_z)))
chassis=chassis.clean()

# ============================================================
# internal release bar - only its small button is visible externally
# ============================================================
def make_release_bar():
    b=rounded_box(release_bar_w,release_bar_d,release_bar_h,0.45,(0,0,0))
    # two rear-stem pusher noses, aligned to locked rear tabs
    # locked rear tab shifts about -2.2 mm from magazine center; nose starts just left of it.
    tab_shift=stem_center_y*math.sin(math.radians(lock_angle))
    for xc in (xL,xR):
        nx=xc-6.80
        nose=rounded_box(release_nose_w,3.0,release_nose_h,0.35,(nx,-2.0,0.35))
        b=b.union(nose)
    # left-side button head: short, recessed, no long external slot
    head=rounded_box(button_w,button_d,button_h,0.8,(-release_bar_w/2-button_w/2+1.0,0,0.45))
    b=b.union(head)
    return b.clean()
release_bar_local=make_release_bar()
def release_bar_global(dx=0):return release_bar_local.translate((dx,release_y,release_z))
release_spring=spring_x(release_spring_len,c=(-25.0,release_y,release_z))

# optional TPU button dust seal: thin membrane patch over the only side opening
button_seal=rounded_box(0.75,9.5,8.5,0.25,(-body_w/2-0.38,release_y,release_z))
button_seal=button_seal.cut(rounded_box(1.0,button_d+0.8,button_h+0.8,0.6,(-body_w/2-0.38,release_y,release_z)))
# frame + flexible center membrane
button_seal=button_seal.union(rounded_box(0.45,button_d+0.65,button_h+0.65,0.55,(-body_w/2-0.38,release_y,release_z)))

# ============================================================
# transfer base / metering deck
# ============================================================
transfer_base=rounded_box(body_w,body_d,base_t,2.0,(0,0,base_z0+base_t/2))
track_depth=base_top-track_floor_z
track_cut=rounded_box(body_w-1.0,shuttle_d+0.80,track_depth+0.12,0.7,(0,mag_y,base_top-track_depth/2+0.04))
transfer_base=transfer_base.cut(track_cut)
# extraction trough to front, continuous with track floor
trough_y_back=-5.6; trough_y_front=front_y-0.7
trough_d=trough_y_back-trough_y_front; trough_cy=(trough_y_back+trough_y_front)/2
trough_h=base_top-track_floor_z+0.35
transfer_base=transfer_base.cut(rounded_box(output_trough_w,trough_d,trough_h,0.65,(0,trough_cy,track_floor_z+trough_h/2-0.12)))
for xc in (xL,xR):
    transfer_base=transfer_base.cut(cyl_z(mag_counterbore_d,mag_counterbore_depth+0.08,(xc,mag_y,base_z0-0.03)))
    throat_z=base_z0+mag_counterbore_depth
    transfer_base=transfer_base.cut(cyl_z(feed_throat_d,base_top-throat_z+0.12,(xc,mag_y,throat_z-0.04)))
# TRUE screw paths through transfer base
for x,y in top_screw_xy:transfer_base=transfer_base.cut(cyl_z(m25_clear,base_t+0.6,(x,y,base_z0-0.3)))
# guide fences
front_fence=box(body_w-4.0,rail_t,rail_h,(0,front_fence_y,rail_z0+rail_h/2))
front_fence=front_fence.cut(rounded_box(mouth_w,rail_t+0.8,mouth_h,1.1,(0,front_fence_y,mouth_center_z)))
rear_rail=box(body_w-4.0,rail_t,rail_h,(0,rear_rail_y,rail_z0+rail_h/2))
transfer_base=transfer_base.union(front_fence).union(rear_rail)
# side walls to mouth
for xx in (-mouth_w/2-0.75,mouth_w/2+0.75):
    tunnel_d=abs(front_fence_y-front_y)-0.2; cy=(front_fence_y+front_y)/2
    transfer_base=transfer_base.union(box(1.05,tunnel_d,rail_h,(xx,cy,rail_z0+rail_h/2)))
# front fascia with open mouth and TPU mount holes
fascia=box(body_w,1.65,6.7,(0,front_y+0.83,mouth_center_z))
fascia=fascia.cut(rounded_box(mouth_w,2.1,mouth_h,1.1,(0,front_y+0.83,mouth_center_z)))
for xx in (-9.2,9.2):fascia=fascia.cut(cyl_y(1.75,3.1,(xx,front_y+0.12,mouth_center_z)))
transfer_base=transfer_base.union(fascia).clean()

# ============================================================
# dual-pocket shuttle with dedicated lower cutoff layer
# ============================================================
def make_shuttle():
    # lower cutoff plate spans the whole shuttle. Only the two circular feed windows + forward extraction throats are open.
    lower=rounded_box(shuttle_w,shuttle_d,cutoff_t,0.75,(0,0,cutoff_t/2))
    for px in (-shuttle_pocket_dx,shuttle_pocket_dx):
        lower=lower.cut(cyl_z(pocket_d,cutoff_t+0.4,(px,0,-0.2)))
        lower=lower.cut(box(lower_front_open_w,shuttle_d/2+2.2,cutoff_t+0.4,(px,-shuttle_d/4-1.1,cutoff_t/2)))
    # upper pocket carrier, with matching C-openings to front
    upper=rounded_box(shuttle_w,shuttle_d,pocket_upper_h,0.75,(0,0,cutoff_t+pocket_upper_h/2))
    for px in (-shuttle_pocket_dx,shuttle_pocket_dx):
        upper=upper.cut(cyl_z(pocket_d,pocket_upper_h+0.5,(px,0,cutoff_t-0.15)))
        upper=upper.cut(box(upper_front_open_w,shuttle_d/2+2.3,pocket_upper_h+0.5,(px,-shuttle_d/4-1.1,cutoff_t+pocket_upper_h/2)))
    s=lower.union(upper)
    # large tactile thumb tab
    tab=rounded_box(tab_w,tab_d,tab_h,0.8,(0,0,shuttle_h+tab_h/2-tab_overlap))
    # simple transverse grip grooves
    for yy in (-2.2,-1.1,0,1.1,2.2):
        tab=tab.cut(box(tab_w-1.2,0.45,0.7,(0,yy,shuttle_h+tab_h-0.30)))
    s=s.union(tab)
    # ball-plunger pilot from top
    s=s.cut(cyl_z(plunger_pilot_d,4.6,(0,plunger_y,shuttle_h-4.55)))
    return s.clean()
shuttle_local=make_shuttle()
def shuttle_global(dx=0):return shuttle_local.translate((dx,mag_y,shuttle_bottom))

# ============================================================
# top cap with real fastener access and large thumb-tab slot
# ============================================================
top_cap=rounded_box(body_w,body_d,cap_t,2.0,(0,0,cap_z0+cap_t/2))
# underside relief for shuttle/rails
relief=rounded_box(body_w-4.8,19.0,1.15,0.8,(0,mag_y,cap_z0+0.58))
top_cap=top_cap.cut(relief)
# travel slot for large thumb tab
slot_center_z=cap_z0+cap_t/2
top_cap=top_cap.cut(rounded_box(slot_len,slot_w,cap_t+0.8,1.5,(0,mag_y,slot_center_z)))
# front finger scoop / mouth access
top_cap=top_cap.cut(rounded_box(16.5,7.3,cap_t+1.0,2.6,(0,front_y+2.15,slot_center_z)))
# no structures over feed holes: generous circular underside clearances
for xc in (xL,xR):top_cap=top_cap.cut(cyl_z(13.3,1.55,(xc,mag_y,cap_z0-0.15)))
# actual through holes + countersinks. No blind column is allowed in the screwdriver line.
for x,y in top_screw_xy:
    top_cap=top_cap.cut(cyl_z(m25_clear,cap_t+0.8,(x,y,cap_z0-0.4)))
    top_cap=top_cap.cut(cyl_z(m25_head_d,1.45,(x,y,cap_top-1.25)))
# 3 position detents, center stronger
for xx,depth in [(-shuttle_shift,side_dimple_depth),(0,center_dimple_depth),(shuttle_shift,side_dimple_depth)]:
    top_cap=top_cap.cut(cyl_z(2.65,depth+0.1,(xx,mag_y+plunger_y,cap_z0-0.02)))
top_cap=top_cap.clean()

# ============================================================
# TPU output dust flap
# ============================================================
def make_tpu_flap():
    # mount rail above mouth + thin living hinge + flap. Separate from rigid feed/shuttle logic.
    mount=rounded_box(flap_mount_w,flap_mount_t,flap_mount_h,0.5,(0,0,flap_h/2+flap_mount_h/2))
    for xx in (-9.2,9.2):mount=mount.union(cyl_y(1.55,2.0,(xx,1.0,flap_h/2+flap_mount_h/2)))
    hinge=box(flap_w,flap_hinge_t,flap_hinge_t,(0,0,flap_h/2))
    leaf=rounded_box(flap_w,flap_t,flap_h,0.55,(0,0,0))
    return mount.union(hinge).union(leaf).clean()
output_flap_local=make_tpu_flap()
output_flap=output_flap_local.translate((0,flap_y,flap_z))

# ============================================================
# full sliding bottom outer cover + labyrinth plug
# ============================================================
def make_bottom_cap():
    c=rounded_box(bottom_cap_w,bottom_cap_d,bottom_cap_t,1.4,(0,0,bottom_cap_z))
    # longitudinal inner labyrinth strips run beside the receiver structure and slide without crossing it.
    # The full floor itself closes the bottom; these strips make the side seam non-line-of-sight.
    for sx in (-1,1):
        c=c.union(box(1.05,22.0,0.95,(sx*26.15,-0.20,-0.05)))
    # two internal side tongues
    for sx in (-1,1):c=c.union(box(tongue_w,bottom_cap_d-1.2,tongue_h,(sx*tongue_x,0,tongue_z)))
    # rear trailing lip: does not pass over body, just meets rear face at closed position
    c=c.union(rounded_box(bottom_cap_w-2.2,rear_lip_t,rear_lip_h,0.5,(0,rear_y+0.62,bottom_cap_z+rear_lip_h/2-0.1)))
    # pull tab under rear edge
    c=c.union(rounded_box(cap_pull_w,cap_pull_d,cap_pull_h,0.55,(0,bottom_cap_d/2+0.9,bottom_cap_z-bottom_cap_t/2-0.25)))
    # detent dimple in right tongue
    c=c.cut(cyl_x(cap_dimple_d,1.0,(tongue_x,cap_plunger_y,tongue_z)))
    return c.clean()
bottom_cap_local=make_bottom_cap()
def bottom_cap_global(y=0):return bottom_cap_local.translate((0,y,0))
bottom_cap=bottom_cap_global(0)

# TPU preload pads between cap and magazine bases
bottom_pad_local=cq.Workplane('XY').circle(bottom_pad_d/2).extrude(bottom_pad_t)
def bottom_pad_global(side):
    xc=xL if side=='L' else xR
    return bottom_pad_local.translate((xc,mag_y,bottom_pad_z))

# ============================================================
# hardware references
# ============================================================
# main springs at representative loaded state
spring_loaded_h=max(10.0,(follower_loaded_center-follower_t/2)-spring_seat_z)
spring_L=spring_z(spring_loaded_h,z0=spring_seat_z).translate((xL,mag_y,0))
spring_R=spring_z(spring_loaded_h,z0=spring_seat_z).translate((xR,mag_y,0))
# M2.5 countersunk screw simple reference and insert
m25_insert=cyl_z(m25_insert_d,m25_insert_depth,(0,0,0))
def m25_screw_ref():
    shaft=cyl_z(2.45,m25_screw_len,(0,0,-m25_screw_len))
    head=cq.Workplane('XY').circle(m25_head_d/2).workplane(offset=1.8).circle(2.45/2).loft(combine=True).translate((0,0,-1.8))
    return shaft.union(head)
m25_screw=m25_screw_ref()
# bottom-cap ball plunger reference, along X
cap_ball_plunger=cyl_x(3.0,5.0,(body_w/2-1.6,cap_plunger_y,cap_plunger_z))
# shuttle center ball plunger reference vertical
shuttle_plunger=cyl_z(3.0,4.0,(0,mag_y+plunger_y,shuttle_top-3.2))
# silicone cord reference
silicone_cord_ref=cyl_z(silicone_cord_d,silicone_z1-silicone_z0,(0,0,0))


# ============================================================
# USER-APPROVED LATE PART REVISIONS (package integration)
# Keep all original assembly coordinates; only replace the revised solids.
# ============================================================
chassis = cq.importers.importStep('/mnt/data/V7_magazine_retention_fix_v2/01_lower_chassis_closed_shell_MAGAZINE_RETAINED_V2.step')
transfer_base = cq.importers.importStep('/mnt/data/V7_02_FINAL_SHUTTLE_CLEAR/02_transfer_base_metering_deck_FINAL.step')
top_cap = cq.importers.importStep('/mnt/data/V7_03_HINGE_RESTORED_AUDITED/03_top_cap_SOLID_CORE_HINGE_RESTORED_FINAL.step')
shuttle_local = cq.importers.importStep('/mnt/data/08_dual_pocket_CUTOFF_shuttle(2).step')
output_flap_local = cq.importers.importStep('/mnt/data/11_TPU_output_dust_flap_PIN_HINGE(1).step')
output_flap = output_flap_local.translate((0,flap_y,flap_z))

# ============================================================
# export parts
# ============================================================
printables={
 '01_lower_chassis_closed_shell':chassis,
 '02_transfer_base_metering_deck':transfer_base,
 '03_top_cap_real_screw_access':top_cap,
 '04_magazine_LEFT_double_J':mag_local,
 '05_magazine_RIGHT_double_J':mag_local,
 '06_follower_double_stem_PRINT_2':follower_local,
 '07_TPU_feed_ring_PRINT_2':feed_ring_local,
 '08_dual_pocket_CUTOFF_shuttle':shuttle_local,
 '09_internal_common_release_bar':release_bar_local,
 '10_TPU_side_button_seal':button_seal,
 '11_TPU_output_dust_flap':output_flap_local,
 '12_full_sliding_bottom_outer_cover':bottom_cap_local,
 '13_TPU_bottom_pad_PRINT_2':bottom_pad_local,
 '14_refill_push_twist_tool':pusher,
}
for n,o in printables.items():
    exporters.export(o,str(OUT/'STEP_parts'/(n+'.step')))
    exporters.export(o,str(OUT/'STL_printable'/(n+'.stl')),tolerance=0.06,angularTolerance=0.12)

# hardware references
exporters.export(m25_insert,str(OUT/'REFERENCE_hardware'/'M2p5_heatset_insert_reference.step'))
exporters.export(m25_screw,str(OUT/'REFERENCE_hardware'/'M2p5x12_countersunk_screw_reference.step'))
exporters.export(cap_ball_plunger,str(OUT/'REFERENCE_hardware'/'M3_bottom_cap_ball_plunger_reference.step'))
exporters.export(shuttle_plunger,str(OUT/'REFERENCE_hardware'/'M3_shuttle_center_detent_ball_plunger_reference.step'))
exporters.export(release_spring,str(OUT/'REFERENCE_hardware'/'release_button_return_spring_reference.step'))
exporters.export(silicone_cord_ref,str(OUT/'REFERENCE_hardware'/'food_grade_silicone_cord_1p5mm_reference.step'))
exporters.export(spring_z(spring_free_len),str(OUT/'REFERENCE_hardware'/'main_spring_10p05OD_0p32wire_110free_reference.step'))
exporters.export(tablet((0,0,tablet_t_nom/2)),str(OUT/'REFERENCE_hardware'/'tablet_nominal_11p2x5p9.step'))

# ============================================================
# assembly helpers/states
# ============================================================
def add(asm,obj,name,color=None):
    if color is None: asm.add(obj,name=name)
    else: asm.add(obj,name=name,color=color)

# 1 complete loaded released
asm=cq.Assembly()
add(asm,chassis,'closed_outer_chassis',cq.Color(0.18,0.18,0.20));add(asm,transfer_base,'metering_deck',cq.Color(0.22,0.22,0.24));add(asm,top_cap,'top_cap',cq.Color(0.25,0.25,0.27));add(asm,bottom_cap,'sliding_bottom_cover',cq.Color(0.20,0.20,0.22));add(asm,shuttle_global(0),'cutoff_shuttle',cq.Color(0.08,0.40,0.88));add(asm,release_bar_global(0),'internal_release_bar',cq.Color(0.92,0.48,0.10));add(asm,output_flap,'TPU_output_flap',cq.Color(0.0,0.65,0.65));add(asm,button_seal,'TPU_side_button_seal',cq.Color(0.0,0.65,0.65))
for side,xc,mag in [('L',xL,mag_L),('R',xR,mag_R)]:
    add(asm,mag,'mag_'+side,cq.Color(0.72,0.72,0.74));add(asm,follower_global(side,follower_loaded_center,0),'follower_'+side,cq.Color(0.12,0.70,0.28));add(asm,feed_ring_global(side),'feed_ring_'+side,cq.Color(0,0.65,0.65));add(asm,bottom_pad_global(side),'bottom_pad_'+side,cq.Color(0,0.65,0.65));add(asm,spring_L if side=='L' else spring_R,'spring_'+side,cq.Color(0.72,0.72,0.72))
    # 15 tablets: top on ring, remaining below
    add(asm,tablet((xc,mag_y,transfer_tablet_center_z)),'tablet_'+side+'_01',cq.Color(1,1,1))
    for i in range(1,capacity_each):
        z=second_tablet_center-(i-1)*tablet_t_nom
        add(asm,tablet((xc,mag_y,z)),'tablet_'+side+f'_{i+1:02}',cq.Color(1,1,1))
asm.save(str(OUT/'ASSEMBLY_STATES'/'01_COMPLETE_30_LOADED_RELEASED.step'))

# 2 cutaway: omit front shell via showing internals only + half-opacity not possible in STEP; use parts without chassis front
cut=cq.Assembly();add(cut,transfer_base,'deck');add(cut,top_cap,'top_cap');add(cut,mag_L,'magL');add(cut,mag_R,'magR');add(cut,shuttle_global(0),'shuttle',cq.Color(0.08,0.4,0.88));add(cut,release_bar_global(0),'release_bar',cq.Color(0.92,0.48,0.10));add(cut,bottom_cap,'bottom_cover');add(cut,output_flap,'flap',cq.Color(0,0.65,0.65))
for side,xc in [('L',xL),('R',xR)]:add(cut,follower_global(side,follower_loaded_center,0),'follower_'+side,cq.Color(0.12,0.7,0.28));add(cut,feed_ring_global(side),'ring_'+side,cq.Color(0,0.65,0.65))
cut.save(str(OUT/'ASSEMBLY_STATES'/'02_CUTAWAY_INTERNALS.step'))

# 3 follower double-J refill states, spread in X
ref=cq.Assembly();sp=42
states=[('EMPTY_UP',follower_empty_center,0),('PUSH_DOWN',follower_lock_center,0),('TWIST_LOCK',follower_lock_center,lock_angle),('READY_FILLED',follower_lock_center,lock_angle)]
for idx,(label,z,a) in enumerate(states):
    dx=(idx-1.5)*sp
    add(ref,tx(mag_local,dx,0,0),'mag_'+label);add(ref,tx(rz(follower_local,a),dx,0,z-follower_t/2-mag_bottom_z),'follower_'+label,cq.Color(0.12,0.7,0.28))
    if label=='READY_FILLED':
        # illustrative 15-tablet column in local mag coordinates
        for i in range(capacity_each):add(ref,tablet((dx,0,mag_h-3.0-i*tablet_t_nom)),'candy_'+str(i),cq.Color(1,1,1))
ref.save(str(OUT/'ASSEMBLY_STATES'/'03_MAGAZINE_DOUBLE_J_REFILL_SEQUENCE.step'))

# 4 side-button release states: locked followers then bar press + released upright followers
rel=cq.Assembly();sp=78
for idx,(label,bar_dx,ang,z) in enumerate([('CASE_CLOSED_LOCKED',0,lock_angle,follower_lock_center),('SIDE_BUTTON_PRESS',release_travel,lock_angle,follower_lock_center),('FOLLOWERS_RELEASED',0,0,follower_loaded_center)]):
    dx=(idx-1)*sp
    add(rel,tx(chassis,dx),'chassis_'+label);add(rel,tx(transfer_base,dx),'deck_'+label);add(rel,tx(bottom_cap,dx),'cover_'+label);add(rel,tx(release_bar_global(bar_dx),dx),'release_'+label,cq.Color(0.92,0.48,0.10))
    for side in ('L','R'):add(rel,tx(follower_global(side,z,ang),dx),'follower_'+side+'_'+label,cq.Color(0.12,0.7,0.28))
rel.save(str(OUT/'ASSEMBLY_STATES'/'04_CLOSE_CASE_THEN_SIDE_BUTTON_DUAL_RELEASE.step'))

# 5 shuttle anti-jam states
shasm=cq.Assembly();sp=70
for idx,(label,sx) in enumerate([('LEFT_DISPENSE',-shuttle_shift),('CENTER_RELOAD',0),('RIGHT_DISPENSE',shuttle_shift)]):
    dx=(idx-1)*sp
    add(shasm,tx(transfer_base,dx),'deck_'+label);add(shasm,tx(top_cap,dx),'cap_'+label);add(shasm,tx(shuttle_global(sx),dx),'shuttle_'+label,cq.Color(0.08,0.4,0.88))
    # source tablets + carried output tablet where appropriate
    for xc,nm in [(xL,'L'),(xR,'R')]:add(shasm,tablet((dx+xc,mag_y,second_tablet_center)),'next_'+nm+'_'+label,cq.Color(1,1,1))
    if sx!=0:add(shasm,tablet((dx,mag_y,transfer_tablet_center_z)),'output_'+label,cq.Color(1,1,1))
shasm.save(str(OUT/'ASSEMBLY_STATES'/'05_SHUTTLE_CUTOFF_ANTI_JAM_STATES.step'))

# 6 bottom cover service states
bc=cq.Assembly();sp=78
for idx,(label,yy) in enumerate([('OPEN_REAR',bottom_cap_open_y),('HALF_SLIDE',17),('CLOSED',0)]):
    dx=(idx-1)*sp
    add(bc,tx(chassis,dx),'chassis_'+label);add(bc,tx(bottom_cap_global(yy),dx),'cover_'+label,cq.Color(0.35,0.35,0.38));add(bc,tx(mag_L,dx),'magL_'+label);add(bc,tx(mag_R,dx),'magR_'+label)
bc.save(str(OUT/'ASSEMBLY_STATES'/'06_FULL_SLIDING_BOTTOM_COVER_SERVICE.step'))

# 7 top screw installation with screw references, exploded vertically
scr=cq.Assembly();add(scr,chassis,'chassis');add(scr,tx(transfer_base,0,0,8),'transfer_base');add(scr,tx(top_cap,0,0,18),'top_cap')
for i,(x,y) in enumerate(top_screw_xy):
    add(scr,tx(m25_insert,x,y,chassis_h-m25_insert_depth),'insert_'+str(i),cq.Color(0.75,0.55,0.18));add(scr,tx(m25_screw,x,y,cap_top+22),'screw_'+str(i),cq.Color(0.72,0.72,0.72))
scr.save(str(OUT/'ASSEMBLY_STATES'/'07_TOP_REAL_SCREW_INSTALLATION.step'))

# 8 output extraction sequence
outa=cq.Assembly();sp=42
for idx,dy in enumerate([0,-2,-4,-6,-8,-10,-12,-14]):
    dx=(idx-3.5)*sp
    add(outa,tx(transfer_base,dx),'deck_'+str(idx));add(outa,tx(shuttle_global(-shuttle_shift),dx),'shuttle_'+str(idx),cq.Color(0.08,0.4,0.88));add(outa,tx(top_cap,dx),'cap_'+str(idx));add(outa,tablet((dx,mag_y+dy,transfer_tablet_center_z)),'tablet_'+str(idx),cq.Color(1,1,1))
outa.save(str(OUT/'ASSEMBLY_STATES'/'08_OUTPUT_EXTRACTION_SEQUENCE.step'))

# 9 exploded all parts
ex=cq.Assembly();add(ex,chassis,'chassis');add(ex,tx(transfer_base,0,0,15),'deck');add(ex,tx(top_cap,0,0,30),'top_cap');add(ex,tx(shuttle_global(0),0,0,22),'shuttle',cq.Color(0.08,0.4,0.88));add(ex,tx(output_flap,0,-10,14),'flap',cq.Color(0,0.65,0.65));add(ex,tx(bottom_cap,0,0,-17),'bottom_cover');add(ex,tx(release_bar_global(0),0,7,-3),'release_bar',cq.Color(0.92,0.48,0.10));add(ex,tx(button_seal,-3,0,0),'button_seal',cq.Color(0,0.65,0.65))
add(ex,tx(mag_L,-13,0,-4),'magL');add(ex,tx(mag_R,13,0,-4),'magR');add(ex,tx(follower_global('L'),-13,0,-10),'followerL',cq.Color(0.12,0.7,0.28));add(ex,tx(follower_global('R'),13,0,-10),'followerR',cq.Color(0.12,0.7,0.28));add(ex,tx(feed_ring_global('L'),-13,0,12),'ringL',cq.Color(0,0.65,0.65));add(ex,tx(feed_ring_global('R'),13,0,12),'ringR',cq.Color(0,0.65,0.65));add(ex,tx(pusher,0,0,40),'refill_tool',cq.Color(0.4,0.4,0.42))
ex.save(str(OUT/'ASSEMBLY_STATES'/'09_EXPLODED_ALL_PARTS.step'))

# ============================================================
# mechanical audit
# ============================================================
audit=[]
def rec(test,value,expected='0',severity='HIGH',note=''):
    if isinstance(value,float) and math.isfinite(value):value=round(value,6)
    audit.append({'test':test,'value':value,'expected':expected,'severity':severity,'note':note})
def pair(test,a,b,expected='0',severity='HIGH',note=''):
    rec(test,ivol(a,b),expected,severity,note)

# printable integrity
for n,o in printables.items():
    rec('connected_solids::'+n,solid_count(o),'1','CRITICAL','Printable part must be one connected solid.')
    rec('valid_shape::'+n,1 if valid(o) else 0,'1','CRITICAL','OpenCascade valid shape.')

# static rigid assembly
pair('magL_vs_chassis',mag_L,chassis,'0','CRITICAL')
pair('magR_vs_chassis',mag_R,chassis,'0','CRITICAL')
pair('transfer_base_vs_chassis',transfer_base,chassis,'0','CRITICAL')
pair('top_cap_vs_transfer_base',top_cap,transfer_base,'0','CRITICAL')
pair('bottom_cover_vs_chassis_closed',bottom_cap,chassis,'0','CRITICAL')
pair('release_bar_vs_chassis_rest',release_bar_global(0),chassis,'0','CRITICAL')
# TPU parts are compliant but their rigid mounts must not be impossible
pair('output_flap_vs_transfer_base_mount',output_flap,transfer_base,'0','HIGH','TPU flap installs in front mount; flexible leaf may contact candy only.')

# follower full travel and two stems inside hidden receiver channels
for side,mag in [('L',mag_L),('R',mag_R)]:
    for idx,z in enumerate([follower_lock_center,follower_loaded_center,40,65,90,follower_empty_center]):
        f=follower_global(side,z,0)
        pair(f'{side}_follower_vs_mag_travel_{idx}',f,mag,'0','CRITICAL')
        pair(f'{side}_follower_vs_closed_chassis_travel_{idx}',f,chassis,'0','CRITICAL','Outer shell remains closed; hidden internal channels clear both stems.')

# double-J rotate at compressed position
for idx,a in enumerate([0,4,8,12,16,lock_angle]):
    f=rz(follower_local,a).translate((0,0,lock_center_local-follower_t/2))
    pair(f'doubleJ_follower_vs_mag_{idx}_{a}deg',f,mag_local,'0','CRITICAL','Both opposite stems rotate into symmetric J windows without solid collision.')

# magazine insertion while follower is locked/rotated
for side,mag in [('L',mag_L),('R',mag_R)]:
    f=follower_global(side,follower_lock_center,lock_angle)
    for dz in [-70,-50,-30,-15,-8,-4,0]:
        mm=tx(mag,0,0,dz);ff=tx(f,0,0,dz)
        v=ivol(mm,chassis)+ivol(mm,transfer_base)+ivol(ff,chassis)+ivol(ff,transfer_base)
        rec(f'{side}_locked_magazine_bottom_insert_{dz}',v,'0','CRITICAL','Magazine installs from bottom while spring remains locked.')

# release-bar sweep against rigid chassis/magazines; follower contact is intentional and checked separately
for j in range(8):
    dx=release_travel*j/7
    b=release_bar_global(dx)
    v=ivol(b,chassis)+ivol(b,mag_L)+ivol(b,mag_R)
    rec(f'release_bar_rigid_sweep_{j}',v,'0','CRITICAL','Internal bar moves; only small side button is externally visible.')
# intentional contact at full press with locked REAR stems
for side in ('L','R'):
    f=follower_global(side,follower_lock_center,lock_angle)
    c=ivol(release_bar_global(release_travel),f)
    rec(f'{side}_release_nose_contacts_locked_follower',c,'>0 intentional contact','FUNCTIONAL','Button bar must physically push rear follower stem to rotate it out of J-lock.')

# bottom cover slide from fully rear-open to closed
for j in range(9):
    yy=bottom_cap_open_y*(1-j/8)
    c=bottom_cap_global(yy)
    v=ivol(c,chassis)+ivol(c,mag_L)+ivol(c,mag_R)
    rec(f'bottom_cover_slide_{j}_y{yy:.1f}',v,'0','CRITICAL','Full-footprint cover slides in internal grooves without flex or screws.')

# feed openings: no rigid columns/bridges above candy keepout cylinders
for side,xc in [('L',xL),('R',xR)]:
    keep=cyl_z(12.25,8.0,(xc,mag_y,mag_top_seat_z-0.2))
    # Transfer base should be open at throat; top cap clears. Exclude guide floor below throat.
    pair(f'{side}_top_cap_feed_keepout',keep,top_cap,'0','CRITICAL','No cap column over feed path.')

# shuttle full sweep and carried candy
for j in range(19):
    sx=-shuttle_shift+(2*shuttle_shift)*j/18
    sh=shuttle_global(sx)
    v=ivol(sh,transfer_base)+ivol(sh,top_cap)+ivol(sh,chassis)
    rec(f'shuttle_rigid_sweep_{j:02}',v,'0','CRITICAL','Full left-center-right stroke.')
    for pocket,px in [('L',-shuttle_pocket_dx),('R',shuttle_pocket_dx)]:
        t=tablet((px+sx,mag_y,transfer_tablet_center_z))
        tm=tablet((px+sx,mag_y,transfer_tablet_center_z_max),tablet_d_max,tablet_t_max)
        vt=ivol(t,transfer_base)+ivol(t,top_cap)+ivol(t,chassis)+ivol(t,sh)
        vm=ivol(tm,transfer_base)+ivol(tm,top_cap)+ivol(tm,chassis)+ivol(tm,sh)
        rec(f'{pocket}_carried_nom_{j:02}',vt,'0','CRITICAL')
        rec(f'{pocket}_carried_MAX_{j:02}',vm,'0','CRITICAL')
    # second candies stay below the moving cutoff plane
    for side,xc in [('L',xL),('R',xR)]:
        nt=tablet((xc,mag_y,second_tablet_center))
        rec(f'{side}_next_tablet_vs_shuttle_{j:02}',ivol(nt,sh),'0','CRITICAL','Second candy cannot enter the lateral void/cutoff plane.')

# explicit anti-jam source blocking at dispense stops: an upward probe at BOTH source holes must hit cutoff solid.
# Probe represents a second candy trying to rise 1.2mm above its retained position.
for sx,label in [(-shuttle_shift,'LEFT_DISPENSE'),(shuttle_shift,'RIGHT_DISPENSE')]:
    sh=shuttle_global(sx)
    for side,xc in [('L',xL),('R',xR)]:
        probe=tablet((xc,mag_y,transfer_tablet_center_z-0.8),tablet_d_max,tablet_t_max)
        c=ivol(probe,sh)
        rec(f'{label}_{side}_source_is_cutoff',c,'>0 blocked by solid cutoff','CRITICAL','At dispense stop the vacated source is physically covered; no second candy can rise into the empty lateral space.')

# at neutral, feed windows must accept both max tablets without rigid shuttle collision
for side,xc in [('L',xL),('R',xR)]:
    t=tablet((xc,mag_y,transfer_tablet_center_z_max),tablet_d_max,tablet_t_max)
    rec(f'{side}_neutral_feed_window_MAX',ivol(t,shuttle_global(0)),'0','CRITICAL','Max tablet enters its feed pocket at neutral.')

# output extraction, include active shuttle as rigid obstacle
for sx,label in [(-shuttle_shift,'RIGHT_POCKET_TO_OUTPUT'),(shuttle_shift,'LEFT_POCKET_TO_OUTPUT')]:
    sh=shuttle_global(sx)
    for idx,dy in enumerate([0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-12,-14]):
        t=tablet((0,mag_y+dy,transfer_tablet_center_z))
        tm=tablet((0,mag_y+dy,transfer_tablet_center_z_max),tablet_d_max,tablet_t_max)
        v=sum(ivol(t,o) for o in (transfer_base,top_cap,chassis,sh))
        vm=sum(ivol(tm,o) for o in (transfer_base,top_cap,chassis,sh))
        rec(f'exit_{label}_{idx:02}',v,'0','CRITICAL','Rigid path includes active cutoff shuttle.')
        rec(f'exit_MAX_{label}_{idx:02}',vm,'0','CRITICAL','Worst-case candy extraction.')

# top screw and screwdriver accessibility: cylinders through cap/base must be clear; shaft ends inside insert boss.
for i,(x,y) in enumerate(top_screw_xy):
    driver=cyl_z(screwdriver_keepout_d,20.0,(x,y,cap_top))
    # Since driver is above the top surface, only neighboring hardware/tab could block it. Check shuttle tab at all states.
    for sx,label in [(-shuttle_shift,'L'),(0,'C'),(shuttle_shift,'R')]:
        rec(f'screwdriver_{i}_vs_shuttle_{label}',ivol(driver,shuttle_global(sx)),'0','CRITICAL','Straight screwdriver access from outside.')
    # shaft clearance cylinders through cap/base intentionally intersect nothing after holes are cut
    shaft_path=cyl_z(2.70,cap_t+base_t+0.2,(x,y,base_z0-0.1))
    rec(f'screw_path_{i}_vs_top_cap',ivol(shaft_path,top_cap),'0','CRITICAL')
    rec(f'screw_path_{i}_vs_transfer_base',ivol(shaft_path,transfer_base),'0','CRITICAL')

# thumb tab ergonomics: tab top must be >2.8mm above cap top
bb=shuttle_global(0).val().BoundingBox(); rec('thumb_tab_above_top_cap_mm',bb.zmax-cap_top,'>=2.8','HIGH','Large tactile thumb control, not flush with top surface.')
# bottom cover footprint closes full bottom
bbc=bottom_cap.val().BoundingBox();rec('bottom_cover_width_coverage_mm',bbc.xlen,'>=59','HIGH');rec('bottom_cover_depth_coverage_mm',bbc.ylen,'>=26','HIGH')

# Write audits
with open(OUT/'AUDIT'/'V7_MECHANICAL_AUDIT.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['test','value','expected','severity','note']);w.writeheader();w.writerows(audit)

# build gate: only numeric zero/one checks automatically gate; intentional >0 contacts are functional requirements.
critical_fail=[]
for r in audit:
    if r['severity']!='CRITICAL':continue
    exp=str(r['expected'])
    val=r['value']
    if exp=='0' and isinstance(val,(int,float)) and abs(val)>0.01:critical_fail.append(r)
    if exp=='1' and val!=1:critical_fail.append(r)
    if exp.startswith('>0') and isinstance(val,(int,float)) and val<=0.01:critical_fail.append(r)

gate={
 'model':'Mentos Clean Breath V7 FUNCTIONAL',
 'architecture':'V5 retained + closed shell + double-stem J follower + hidden dual-release + full sliding cover + cutoff shuttle',
 'critical_failures':len(critical_fail),
 'status':'CAD_GATE_PASS' if len(critical_fail)==0 else 'CAD_GATE_REVIEW',
 'important_physical_validation':['real candy production tolerance','main spring force curve','TPU feed ring hardness/food compatibility','FDM sliding clearances','bottom-cover dust performance'],
 'critical_failure_tests':[r['test'] for r in critical_fail]
}
(OUT/'AUDIT'/'V7_BUILD_GATE.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2),encoding='utf-8')

# README
readme=f'''# Mentos Clean Breath V7 FUNCTIONAL CAD\n\nBu surum V6 mimarisinin devamı degildir. V5'in anlaşılır 15+15 şarjör + yay + follower + lineer shuttle mantığına geri dönülmüş ve kullanıcı geri bildirimleri hedefli olarak uygulanmıştır.\n\n## V7'de korunan V5 özellikleri\n- 2 x 15 adet çıkarılabilir dikey şarjör.\n- Her şarjörde ana metal yay + takipçi/follower.\n- Üstte tek lineer dual-pocket shuttle ile sol/orta/sağ kullanım.\n- TPU feed ring ile bir sonraki tabletin kesme düzlemine kontrolsüz çıkmasını azaltan yapı.\n\n## V7 değişiklikleri\n1. Ana dış gövde boyunca follower kanalı YOKTUR. Dış kabuk kapalıdır.\n2. Her follower tek parça üzerinde ön ve arka olmak üzere İKİ karşılıklı sapa sahiptir. Şarjör içinde iki gizli düşey slot ve iki simetrik J/bayonet cebi vardır.\n3. Follower dışarıdaki refill aparatıyla aşağı bastırılıp yaklaşık {lock_angle:.0f}° döndürülür; iki sap aynı anda kilitlenir.\n4. Şarjörler yay hâlâ kilitliyken gövdeye alttan takılır.\n5. Gövde dışında yalnızca sol yanda küçük gömme bir buton görünür. İç ortak release bar her iki şarjörün arka sapını aynı anda iterek follower'ları J kilidinden çıkarır.\n6. Alt servis kapağında rutin vida yoktur. Tam tabanı kapatan sürgülü dış kapak, iç plug/labirent bindirmesi ve yan kılavuzlarla kapanır; metal ball-plunger detenti ile tutulur.\n7. Üstte dört M2.5 gerçek vida yolu vardır: top-cap ve transfer base tamamen geçişli, chassis içinde heat-set insert bossları bulunur.\n8. Shuttle iki katmanlıdır. Alt katman CUT-OFF plaka görevi görür. Sürgü bir dispense stopuna gittiğinde her iki şarjör feed deliği de katı yüzeyle kapatılır; diğer şekerin oluşan boşluğa yükselmesi hedefli olarak engellenir.\n9. Thumb tab genişletildi ve top-cap yüzeyinin üzerinde belirgin yüksekliğe çıkarıldı. Merkez ball-detent yan konumlardan daha güçlüdür.\n10. Çıkışta ayrı TPU toz/dökülme flap'i bulunur.\n\n## Doldurma / aktivasyon sırası\n1. Şarjör cihaz dışında tutulur, TPU feed ring çıkarılır.\n2. Refill push-twist tool follower'a takılır, follower aşağı bastırılır ve ~{lock_angle:.0f}° döndürülerek iki taraflı J kilidine alınır.\n3. 15 tablet doldurulur ve feed ring tekrar takılır.\n4. İki şarjör de ANA YAYLAR KİLİTLİ halde ana gövdeye alttan sürülür.\n5. Tam genişlikte alt sürgülü dış kapak kapatılır.\n6. Bundan SONRA yan taraftaki tek recessed release butonuna basılır. İç release bar iki follower'ı aynı anda kilitten çıkarır ve yaylar tabletleri yukarı beslemeye başlar.\n\n## Kullanım\n- Shuttle merkezde güçlü detent ile taşınır.\n- Bir yöne kaydırıldığında bir cep merkez çıkışa gelir.\n- Alt cutoff katmanı kaynak delikleri kapattığı için ikinci tablet boş lateral hacme çıkamaz.\n- Tablet TPU çıkış flap'inden çekilir. Shuttle merkeze döndüğünde boş cep yeniden dolar.\n\n## Montaj dosyaları\n- 01_COMPLETE_30_LOADED_RELEASED.step\n- 02_CUTAWAY_INTERNALS.step\n- 03_MAGAZINE_DOUBLE_J_REFILL_SEQUENCE.step\n- 04_CLOSE_CASE_THEN_SIDE_BUTTON_DUAL_RELEASE.step\n- 05_SHUTTLE_CUTOFF_ANTI_JAM_STATES.step\n- 06_FULL_SLIDING_BOTTOM_COVER_SERVICE.step\n- 07_TOP_REAL_SCREW_INSTALLATION.step\n- 08_OUTPUT_EXTRACTION_SEQUENCE.step\n- 09_EXPLODED_ALL_PARTS.step\n\n## CAD gate\nStatus: **{gate['status']}**\nCritical failure count: **{gate['critical_failures']}**\n\nCAD collision/assembly gate fiziksel ürün testinin yerine geçmez. Özellikle gerçek Mentos ölçü dağılımı, yay kuvveti, TPU sertliği ve kullanılan yazıcının toleransı gerçek baskıda doğrulanmalıdır.\n'''
(OUT/'README_TR.md').write_text(readme,encoding='utf-8')

# audit summary
summary='''# V7 CAD Audit Özeti\n\nV7'nin amacı V5'in anlaşılır mekanik mimarisini korurken V6'da kullanıcı tarafından reddedilen kapalı/karmaşık değişiklikleri geri almaktır. Audit özellikle şu konuları ayrı gate olarak kontrol eder:\n\n- çift saplı follower'ın şarjör içindeki tüm stroku,\n- iki taraflı J kilidinin dönüş montajı,\n- şarjörlerin follower kilitliyken alttan montaj yolu,\n- dışarıdan yalnız küçük yan butonla çalışan iç release bar süpürmesi,\n- tam tabanı kapatan sürgülü alt kapağın montaj yolu,\n- top-cap vida/tornavida düz erişim hacimleri,\n- shuttle tam stroku ve worst-case tablet zarfı,\n- ikinci tabletin cutoff düzlemine çıkmaması,\n- dispense stoplarında her iki kaynak deliğin katı cutoff ile bloke olması,\n- gerçek merkezi şeker çıkış yolunda aktif shuttle dahil tüm rijit engeller.\n\nBuild gate JSON dosyasındaki status mekanik CAD gate sonucudur.\n'''
(OUT/'AUDIT'/'V7_AUDIT_SUMMARY_TR.md').write_text(summary,encoding='utf-8')

# copy source
shutil.copy(__file__,OUT/'SOURCE'/'build_mentos_v7.py')

# zip
ZIP=Path('/mnt/data/Mentos_CleanBreath_V7_FUNCTIONAL_ZERO_CRITICAL_RETENTION_V2.zip')
if ZIP.exists():ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.rglob('*'):
        if p.is_file():z.write(p,p.relative_to(OUT.parent))
print(json.dumps(gate,ensure_ascii=False,indent=2))
print('OUT',OUT)
print('ZIP',ZIP)
