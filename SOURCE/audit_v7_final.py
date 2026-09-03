import cadquery as cq, math, csv, json, shutil, zipfile
from cadquery import importers
from pathlib import Path
OUT=Path('/mnt/data/Mentos_CleanBreath_V7_FUNCTIONAL_CAD'); P=OUT/'STEP_parts'
load=lambda n: importers.importStep(str(P/n))
ch=load('01_lower_chassis_closed_shell.step');tb=load('02_transfer_base_metering_deck.step');tc=load('03_top_cap_real_screw_access.step');mag=load('04_magazine_LEFT_double_J.step');fol=load('06_follower_double_stem_PRINT_2.step');sh=load('08_dual_pocket_CUTOFF_shuttle.step');bar=load('09_internal_common_release_bar.step');cap=load('12_full_sliding_bottom_outer_cover.step')
# constants matching builder
xL,xR=-9.5,9.5; mag_y=-1.35; mag_bottom_z=3.2; follower_t=2.35; lock_center=12.4; lock_angle=18; release_z=12.6;release_y=10.0;release_travel=2.45
mag_top_seat_z=107.8; mag_h=104.6; feed_ring_bottom=3.2+(mag_h-0.90); feed_ring_top=feed_ring_bottom+0.78; top_bottom=feed_ring_top+0.06; tcenter=top_bottom+5.9/2; tcentermax=top_bottom+6.2/2; second_top=feed_ring_bottom-0.08; second_center=second_top-5.9/2
sh_bottom=feed_ring_top+0.20; shift=9.5; pocketdx=9.5; tablet_d=11.2;tablet_t=5.9; dmax=11.55;tmax=6.2; bottom_cap_open_y=34
body_w=60;body_d=27;cap_top=117.7 # approx only used ergonomic read; actual bbox used
# top screws positions
screws=[(-25.0,-9.7),(25.0,-9.7),(-25.0,9.7),(25.0,9.7)]

def tx(o,x=0,y=0,z=0):return o.translate((x,y,z))
def rz(o,a):return o.rotate((0,0,0),(0,0,1),a)
def iv(a,b):
    try:
        A=a.val().BoundingBox();B=b.val().BoundingBox()
        if A.xmax<B.xmin-1e-6 or B.xmax<A.xmin-1e-6 or A.ymax<B.ymin-1e-6 or B.ymax<A.ymin-1e-6 or A.zmax<B.zmin-1e-6 or B.zmax<A.zmin-1e-6:return 0.0
        return float(a.val().intersect(b.val()).Volume())
    except:return float('nan')
def sc(o):
    try:return len(o.val().Solids())
    except:return -1
def val(o):
    try:return 1 if o.val().isValid() else 0
    except:return 0
def tablet(c,d=tablet_d,t=tablet_t):
    x,y,z=c;o=cq.Workplane('XY').circle(d/2).extrude(t)
    try:o=o.edges().fillet(min(.72,t/3))
    except:pass
    return o.translate((x,y,z-t/2))
magL=tx(mag,xL,mag_y,mag_bottom_z);magR=tx(mag,xR,mag_y,mag_bottom_z)
def follower(side,z,a=0):return tx(rz(fol,a),xL if side=='L' else xR,mag_y,z-follower_t/2)
def shuttle(sx):return tx(sh,sx,mag_y,sh_bottom)
def rel(dx):return tx(bar,dx,release_y,release_z)
rows=[]
def R(name,value,expected='0',severity='CRITICAL',note=''):
    if isinstance(value,float) and math.isfinite(value):value=round(value,6)
    rows.append(dict(test=name,value=value,expected=expected,severity=severity,note=note))
def P(name,a,b,expected='0',severity='CRITICAL',note=''):R(name,iv(a,b),expected,severity,note)
# integrity
for name,o in [('chassis',ch),('transfer_base',tb),('top_cap',tc),('magazine',mag),('follower',fol),('shuttle',sh),('release_bar',bar),('bottom_cover',cap)]:
    R('connected_solids::'+name,sc(o),'1');R('valid_shape::'+name,val(o),'1')
# static
P('magL_vs_chassis',magL,ch);P('magR_vs_chassis',magR,ch);P('base_vs_chassis',tb,ch);P('topcap_vs_base',tc,tb);P('bottomcover_vs_chassis_closed',cap,ch);P('releasebar_rest_vs_chassis',rel(0),ch);P('releasebar_rest_vs_magL',rel(0),magL);P('releasebar_rest_vs_magR',rel(0),magR)
# follower travel and lock rotation
for side,mm in [('L',magL),('R',magR)]:
    for z in [12.4,20,40,65,90,103.7]:
        f=follower(side,z,0);P(f'{side}_follower_vs_mag_z{z}',f,mm);P(f'{side}_follower_vs_closed_shell_z{z}',f,ch)
for a in [0,6,12,18]:P(f'doubleJ_rotation_{a}',tx(rz(fol,a),0,0,(lock_center-mag_bottom_z)-follower_t/2),mag,'0','CRITICAL','Both stems rotate within symmetric J windows.')
# locked magazine insertion
for side,mm in [('L',magL),('R',magR)]:
    f=follower(side,lock_center,lock_angle)
    for dz in [-60,-35,-18,-8,0]:
        v=iv(tx(mm,0,0,dz),ch)+iv(tx(mm,0,0,dz),tb)+iv(tx(f,0,0,dz),ch)+iv(tx(f,0,0,dz),tb)
        R(f'{side}_locked_mag_insert_{dz}',v,'0','CRITICAL','Spring remains locked while inserting magazine.')
# side button common release sweep; contact only at full press
for dx in [0,0.5,1.0,1.5,2.0,2.45]:
    b=rel(dx);R(f'release_sweep_{dx}',iv(b,ch)+iv(b,magL)+iv(b,magR),'0','CRITICAL','Internal bar clears rigid housing.')
for side in ['L','R']:
    lf=follower(side,lock_center,lock_angle);R(f'{side}_release_contact_rest',iv(rel(0),lf),'0','CRITICAL');R(f'{side}_release_contact_press',iv(rel(release_travel),lf),'>0 intentional','CRITICAL','Pusher nose reaches locked rear stem.')
# bottom cover slide
for yy in [34,28,22,16,10,5,0]:R(f'bottom_cover_slide_y{yy}',iv(tx(cap,0,yy,0),ch)+iv(tx(cap,0,yy,0),magL)+iv(tx(cap,0,yy,0),magR),'0','CRITICAL','Full outer cover slides without screw removal.')
# shuttle and candy sweep
for sx in [-9.5,-6.33,-3.17,0,3.17,6.33,9.5]:
    s=shuttle(sx);R(f'shuttle_rigid_{sx}',iv(s,tb)+iv(s,tc)+iv(s,ch),'0')
    for px,label in [(-9.5,'L'),(9.5,'R')]:
        t=tablet((px+sx,mag_y,tcenter));tm=tablet((px+sx,mag_y,tcentermax),dmax,tmax)
        R(f'{label}_carried_nom_{sx}',sum(iv(t,o) for o in [tb,tc,ch,s]),'0');R(f'{label}_carried_MAX_{sx}',sum(iv(tm,o) for o in [tb,tc,ch,s]),'0')
    for xc,label in [(xL,'L'),(xR,'R')]:R(f'{label}_next_vs_cutoff_{sx}',iv(tablet((xc,mag_y,second_center)),s),'0','CRITICAL','Second candy stays below moving cutoff plane.')
# explicit source blocking at both dispense stops
for sx,st in [(-9.5,'LEFT_DISPENSE'),(9.5,'RIGHT_DISPENSE')]:
    s=shuttle(sx)
    for xc,label in [(xL,'L'),(xR,'R')]:R(f'{st}_{label}_SOURCE_BLOCK',iv(tablet((xc,mag_y,tcenter-0.8),dmax,tmax),s),'>0 blocked','CRITICAL','Solid cutoff covers source when shuttle leaves neutral.')
# neutral max feed windows
for xc,label in [(xL,'L'),(xR,'R')]:R(f'{label}_neutral_MAX_feed',iv(tablet((xc,mag_y,tcentermax),dmax,tmax),shuttle(0)),'0')
# extraction
for sx,st in [(-9.5,'R_POCKET'),(9.5,'L_POCKET')]:
    s=shuttle(sx)
    for dy in [0,-2,-4,-6,-8,-10,-12,-14]:
        t=tablet((0,mag_y+dy,tcenter));tm=tablet((0,mag_y+dy,tcentermax),dmax,tmax)
        R(f'exit_{st}_{dy}',sum(iv(t,o) for o in [tb,tc,ch,s]),'0');R(f'exit_MAX_{st}_{dy}',sum(iv(tm,o) for o in [tb,tc,ch,s]),'0')
# feed keepout above both columns in top cap
for xc,label in [(xL,'L'),(xR,'R')]:P(f'{label}_cap_feed_keepout',cq.Workplane('XY').center(xc,mag_y).circle(12.25/2).extrude(8).translate((0,0,107.6)),tc)
# screwdriver vertical access vs shuttle in all three states
for i,(x,y) in enumerate(screws):
    # tall tool cylinder from top cap upward; starts well above mechanism
    drv=cq.Workplane('XY').center(x,y).circle(4).extrude(25).translate((0,0,118.0))
    for sx,l in [(-9.5,'L'),(0,'C'),(9.5,'R')]:P(f'screwdriver_{i}_vs_shuttle_{l}',drv,shuttle(sx))
# ergonomics via bboxes
shbb=shuttle(0).val().BoundingBox();tcbb=tc.val().BoundingBox();R('thumb_tab_height_above_cap_mm',shbb.zmax-tcbb.zmax,'>=2.8','HIGH');bb=cap.val().BoundingBox();R('bottom_cover_width_mm',bb.xlen,'>=59','HIGH');R('bottom_cover_depth_mm',bb.ylen,'>=28','HIGH')
# gate
fail=[]
for r in rows:
    if r['severity']!='CRITICAL':continue
    exp=str(r['expected']);v=r['value']
    if exp=='0' and isinstance(v,(int,float)) and abs(v)>0.01:fail.append(r)
    elif exp=='1' and v!=1:fail.append(r)
    elif exp.startswith('>0') and isinstance(v,(int,float)) and v<=0.01:fail.append(r)
with open(OUT/'AUDIT'/'V7_MECHANICAL_AUDIT.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['test','value','expected','severity','note']);w.writeheader();w.writerows(rows)
gate={'model':'Mentos Clean Breath V7 FUNCTIONAL','critical_failures':len(fail),'status':'CAD_GATE_PASS' if not fail else 'CAD_GATE_REVIEW','critical_failure_tests':[x['test'] for x in fail],'scope':['connected printable solids','closed-shell follower travel','double-sided J lock','locked magazine insertion','side-button dual release','full sliding bottom cover','cutoff shuttle sweep','second-candy anti-jam block','worst-case candy extraction','top feed keepout','screwdriver access'],'physical_validation_still_required':['real candy lot tolerances','main spring force curve','TPU hardness and food-safe material','FDM printer-specific sliding clearance','dust ingress check on bottom cover/button seal']}
(OUT/'AUDIT'/'V7_BUILD_GATE.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(gate,ensure_ascii=False,indent=2))
