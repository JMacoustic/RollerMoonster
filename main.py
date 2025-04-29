# Source: https://github.com/SNU-IntelligentMotionLab/SNU_ComputerGraphics_/blob/main/main.py
# This script is based on above repository and adjusted for additional functionalities

import pyglet 
from pyglet.gl import *
import numpy as np
from scripts.rail import Rail, Cart
from scripts.spline import NatCubeSpline
from scripts import camera, utils


width  = 1500
height = 1000

window = pyglet.window.Window(width, height, resizable=True, caption="Roller-Moonster")
program = pyglet.graphics.get_default_shader()
groundBatch = pyglet.graphics.Batch()
railBatch = pyglet.graphics.Batch()
event = utils.EventWatcher()
counter=utils.TimeCounter(0)

ground = pyglet.image.load('texture/ground2.png')
ground_1 = pyglet.sprite.Sprite(img=ground, x=0, y=0, z=-4, batch=groundBatch)
ground_1.scale_x = 0.05
ground_1.scale_y = 0.05
ground_2 = pyglet.sprite.Sprite(img=ground, x=0, y=0, z=-4, batch=groundBatch)
ground_2.scale_x = 0.05
ground_2.scale_y = 0.05
ground_2.rotation = 90
ground_3 = pyglet.sprite.Sprite(img=ground, x=0, y=0, z=-4, batch=groundBatch)
ground_3.scale_x = 0.05
ground_3.scale_y = 0.05
ground_3.rotation = 180
ground_4 = pyglet.sprite.Sprite(img=ground, x=0, y=0, z=-4, batch=groundBatch)
ground_4.scale_x = 0.05
ground_4.scale_y = 0.05
ground_4.rotation = -90


@window.event
def on_resize(width, height):
    camera.resize( window, width, height )
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	window.clear()
	camera.apply(window)
	groundBatch.draw()
	railBatch.draw()

@window.event
def on_key_press( key, mods ):	
	if key==pyglet.window.key.Q:
		pyglet.app.exit()
	
	if key==pyglet.window.key._1:
		event.thirdview = False
	
	if key==pyglet.window.key._3:
		event.thirdview = True
		camera.detach_spline()
	
@window.event
def on_mouse_release( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed
	mouseMovePressed   = False
	mouseRotatePressed = False
	mouseDollyPressed   = False

@window.event
def on_mouse_press( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed

	if button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_SHIFT:
		mouseMovePressed   = True
		mouseRotatePressed = False
		mouseDollyPressed   = False
	elif button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_CTRL:
		mouseMovePressed   = False
		mouseRotatePressed = False
		mouseDollyPressed   = True
	elif button & pyglet.window.mouse.LEFT:
		camera.beginRotate(x, y)
		mouseMovePressed   = False
		mouseRotatePressed = True
		mouseDollyPressed   = False

@window.event
def on_mouse_drag(x, y, dx, dy, button, mods ):	
	if mouseRotatePressed:
		camera.rotate(x, y)
	elif mouseMovePressed:
		camera.move(dx/width, dy/height, 0.0)
	elif mouseDollyPressed:
		camera.zoom(dy/height)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera.zoom(z=-scroll_y*0.1)  # Use scroll_y for zooming


def update(dt):
	counter.update_time(dt)

	if s.value >= smax:
		s.reset()
	s.add(spline.speed(u.value) * dt)
	u.value = spline.inv_length(s.value)
	cart.move(u.value)
	
	if event.thirdview == False:
		camera.follow_spline(spline, u.value, frame=frame)
	elif event.thirdview ==True:
		camera.remember_thirdview()
		
		
passing_points = np.array([
    [0, 0, 0],
    [-1, -2, 0],
	[1, -2, -1],
    [2, 2, 0],
    [1, 3, 5],
    [1, 2, 5],
    [4, 1, 5],
    [4.5, 1.5, 3],
	[5, 4, 1],
	[4.5, 6, 2],
	[4, 4, 4],
	[3.5, 4, 1],
    [3, 6, 0],
	[1, 5, -1],
    [3, 1, 0],
    [0, 0, 0]
])

# initialize spline, rail, and cart
frame = "frenet_frame"
spline = NatCubeSpline(passing_points)
rail = Rail(spline=spline, thickness=0.1, width = 1, n_cylinders=500, n_plates=50, batch=railBatch, frame=frame)
cart = Cart(spline=spline, batch=railBatch, frame=frame)

# initialize simulation parameters
s = utils.value(0)
u = utils.value(0)
tmax = 100 # Stop after 100 seconds
smax = spline.length(spline.umax) # to reset length after 1 loop

pyglet.clock.schedule_interval(update, 1/60)
glClearColor(0.529, 0.808, 0.922, 1.0)
glEnable(GL_DEPTH_TEST)
glClearDepth(1.0)
glDepthFunc(GL_LESS)

camera.resize( window, width, height )	
pyglet.app.run()