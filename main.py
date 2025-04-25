# Source: https://github.com/SNU-IntelligentMotionLab/SNU_ComputerGraphics_/blob/main/main.py
# This script is based on above repository and adjusted for additional functionalities

import pyglet 
from scripts import camera, motion, utils
from scripts.snakemodel import Snake
from pyglet.gl import *
import math

width  = 1500
height = 1000

window = pyglet.window.Window(width, height, resizable=True, caption="Snake crawls and attacks")
program = pyglet.graphics.get_default_shader()
snakeBatch = pyglet.graphics.Batch()
groundBatch = pyglet.graphics.Batch()

ground = pyglet.image.load('texture/ground2.png')
ground_1 = pyglet.sprite.Sprite(img=ground, x=0, y=-18, z=-0.1, batch=groundBatch)
ground_1.scale_x = 0.05
ground_1.scale_y = 0.05
ground_2 = pyglet.sprite.Sprite(img=ground, x=0, y=-18, z=-0.1, batch=groundBatch)
ground_2.scale_x = 0.05
ground_2.scale_y = 0.05
ground_2.rotation = 90
ground_3 = pyglet.sprite.Sprite(img=ground, x=0, y=-18, z=-0.1, batch=groundBatch)
ground_3.scale_x = 0.05
ground_3.scale_y = 0.05
ground_3.rotation = 180
ground_4 = pyglet.sprite.Sprite(img=ground, x=0, y=-18, z=-0.1, batch=groundBatch)
ground_4.scale_x = 0.05
ground_4.scale_y = 0.05
ground_4.rotation = -90


tailcounter = utils.TimeCounter(t0=0)
stopcounter = utils.TimeCounter(t0=0)
liftcounter = utils.TimeCounter(t0=0)
lowercounter = utils.TimeCounter(t0=0)
attackcounter = utils.TimeCounter(t0=0)
event = utils.EventWatcher()

color1 = (0.2, 1.0, 1.0, 1.0)
color2 = (1.0, 1.0, 0.2, 1.0)
newSnake = Snake(color1, color2, batch = snakeBatch)

@window.event
def on_resize(width, height):
    camera.resize( window, width, height )
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	window.clear()
	camera.apply(window)
	snakeBatch.draw()
	groundBatch.draw()

@window.event
def on_key_press( key, mods ):	
	if key==pyglet.window.key.Q:
		pyglet.app.exit()

	if key == pyglet.window.key._1 and event.wavetail==False:
		print("key 1 pressed. Start moving")
		tailcounter.reset()
		event.wavetail = True

	if key==pyglet.window.key._2 and event.wavetail==True and event.moving == True:
		print("key 2 pressed. Stop moving")
		stopcounter.reset()
		event.wavetail = False
	
	if key==pyglet.window.key._3 and event.raisehead==False and event.headsup==False:
		print("key 3 pressed. Start lifting head")
		liftcounter.reset()
		event.raisehead = True
		event.lowerhead = False

	if key==pyglet.window.key._4 and event.attack==False:
		if event.headsup==True and event.lowerhead==False:
			print("key 4 pressed. Start attack")
			attackcounter.reset()
			event.attack = True
		else:
			print("To attack, first lift the head up by pressing key 3")

	if key==pyglet.window.key._5 and event.lowerhead==False and event.headsup==True:
		print("key 5 pressed. Start lowering head")
		lowercounter.reset()
		event.lowerhead = True
		event.raisehead = False
	
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
	orientation = motion.rest_angles
	wave_orient = motion.null_angles

	if event.wavetail==True:
		tailcounter.update_time(dt=dt)
		wave_orient = motion.sinwaveSnake(current_t=tailcounter.t, height=0.3, phase=0, width=math.pi/4, frequency=5)
		wave_orient = motion.interpolation(motion.null_angles, wave_orient, tailcounter.t) # start moving in 1 second
		orientation = motion.superposition(wave_orient, motion.rest_angles)
		ground_1.rotation += 4.3*dt 
		ground_2.rotation += 4.3*dt
		ground_3.rotation += 4.3*dt
		ground_4.rotation += 4.3*dt
		if tailcounter.t > 1:
			event.moving = True

	if event.wavetail==False and event.moving == True:
		tailcounter.update_time(dt=dt)
		stopcounter.update_time(dt=dt)
		wave_orient = motion.sinwaveSnake(current_t=tailcounter.t, height=0.3, phase=0, width=math.pi/4, frequency=5)
		wave_orient = motion.interpolation(wave_orient, motion.null_angles, stopcounter.t) # start moving in 1 second
		orientation = motion.superposition(wave_orient, motion.rest_angles)
		# orientation = motion.interpolation(orientation, motion.rest_angles, stopcounter.t) # start moving in 1 second
		ground_1.rotation += (4-2*stopcounter.t)*dt 
		ground_2.rotation += (4-2*stopcounter.t)*dt
		ground_3.rotation += (4-2*stopcounter.t)*dt
		ground_4.rotation += (4-2*stopcounter.t)*dt
		if stopcounter.t > 1:
			event.moving = False

	if event.raisehead==True:
		liftcounter.update_time(dt=dt)
		end_t1 = 1
		lift_orient = motion.raisehead(start_angles=motion.rest_angles, current_t=liftcounter.t, start_t=0, end_t=end_t1)
		if liftcounter.t > end_t1:
			event.headsup = True
		orientation = motion.superposition(wave_orient, lift_orient)

	if event.lowerhead==True and event.headsup==True:
		lowercounter.update_time(dt=dt)
		end_t2 = 1
		lower_orient = motion.lowerhead(start_angles=motion.raisehead_angles, current_t=lowercounter.t, start_t=0, end_t=end_t2)
		if lowercounter.t > end_t2:
			event.headsup=False
		orientation = motion.superposition(wave_orient, lower_orient)
	
	if event.attack==True and event.headsup==True:
		attackcounter.update_time(dt=dt)
		end_t3=0.5
		attack_orient = motion.attack(start_angles=motion.raisehead_angles, current_t=attackcounter.t, start_t=0, end_t=end_t3)
		if attackcounter.t > end_t3:
			event.attack=False
			event.headsup=True
		orientation = motion.superposition(wave_orient, attack_orient)


	newSnake.set_orientation(orientation)



pyglet.clock.schedule_interval(update, 1/60)
glClearColor(0.0, 0.1, 0.3, 1.0)
glEnable(GL_DEPTH_TEST)
glClearDepth(1.0)
glDepthFunc(GL_LESS)

camera.resize( window, width, height )	
pyglet.app.run()