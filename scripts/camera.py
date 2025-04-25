# Source: https://github.com/snumrl/TrackballViewer/blob/main/camera.py
# This script is adapted from the above repository.


from pyglet.gl import *
from pyglet.math import Mat4, Vec3, Quaternion

import math

aspectRatio = 1.0
nearPlane   = 0.1
farPlane    = 10000.0
  
beginu, beginv   = 0, 0
height, width    = 0, 0

curquat    = [-0.36315166267487914, -0.2656206482393097, 0.48607924457270246, 0.7491952409893102]
lastquat   = [1,0,0,0]
tx, ty, tz = 0.0, 0.0, 0.0
dolly      = 8.0

TRACKBALLSIZE = 0.6


def resize( window, w, h ):
    global height, width, aspectRatio
    
    height = int(h)
    width  = int(w)
    aspectRatio = float(width)/float(height)
    
    window.viewport = ( 0, 0, width, height )
    window.projection = Mat4.perspective_projection(aspectRatio, z_near=0.1, z_far=255)


def move( dx, dy, dz ):
    global tx, ty, tz
    tx += 4.0*dx
    ty += 4.0*dy
    tz += 4.0*dz

    
def beginRotate( u, v ):
    global beginu, beginv, moving
    
    beginu   = u
    beginv   = v


def rotate( u, v ):
    global beginu, beginv, curquat
    
    lastquat = trackball( 
        (width  - 2.0 * beginu) / width,
        (height - 2.0 * beginv) / height,
        (width  - 2.0 * u) / width,
        (height - 2.0 * v) / height )

    beginu = u
    beginv = v
    curquat = multiply( curquat, lastquat )
    
    
def zoom( z ):
    global dolly
    dolly += 15.0*z
    
    
def apply(window):
    global tx, ty, tz
    global dolly, curquat
    
    q = Quaternion(curquat[0],curquat[1],curquat[2],curquat[3])
        
    window.view = Mat4.from_translation(Vec3(tx,ty,tz)) @ Mat4.from_translation(Vec3(0.0, 0.0, -dolly)) @ Quaternion.to_mat4(q)
      

def trackball( p1x, p1y, p2x, p2y ):
    if p1x==p2x and p1y==p2y:
        return [1.0, 0.0, 0.0, 0.0]
        
    p1 = [p1x,p1y,project_to_sphere(TRACKBALLSIZE,p1x,p1y)]
    p2 = [p2x,p2y,project_to_sphere(TRACKBALLSIZE,p2x,p2y)]

    a  = [p2[1]*p1[2]-p2[2]*p1[1],
          p2[2]*p1[0]-p2[0]*p1[2],
          p2[0]*p1[1]-p2[0]*p1[1]]
    d  = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])
    t  = math.sqrt(d[0]**2+d[1]**2+d[2]**2) / (2.0*TRACKBALLSIZE)
    
    if t> 1.0: t =  1.0
    if t<-1.0: t = -1.0
    phi = -5.0 * math.asin(t)
    
    return axis_to_quat( a, phi )
    

def axis_to_quat( a, phi ):
    l = math.sqrt(a[0]**2+a[1]**2+a[2]**2)
    s = math.sin(phi/2.0)
    c = math.cos(phi/2.0)
    return [c, a[0]*s/l, a[1]*s/l, a[2]*s/l]


def project_to_sphere( r, x, y ):
    d = math.sqrt( x*x + y*y )
    if d < r*0.70710678118654752440:
        z = math.sqrt( r*r - d*d )
    else:
        t = r / 1.41421356237309504880
        z = t*t / d
    return z
    
    
def multiply( q1, q2 ):
    d = [q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3],
         q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2],
         q1[0]*q2[2] + q1[2]*q2[0] + q1[3]*q2[1] - q1[1]*q2[3],
         q1[0]*q2[3] + q1[3]*q2[0] + q1[1]*q2[2] - q1[2]*q2[1]]
    
    l = math.sqrt(d[0]**2+d[1]**2+d[2]**2+d[3]**2)
    d[0] /= l
    d[1] /= l
    d[2] /= l
    d[3] /= l
    return d

