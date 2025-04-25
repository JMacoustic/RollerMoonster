from scripts import geometry
from pyglet.math import Mat4, Vec3
from math import pi

class Snake:
    "this class generate body shapes of a snake components, and link them in hierarchy."
    def __init__(self, color1, color2, batch):
        self.snakeBatch = batch
        self.default_angles = { # format:[bend, tilt]
            "wb1" : Mat4(), # world to body
            "b1n1" : [0, 0], # body1 > neck1  
            "n1n2" : [0, 0], # neck1 > neck2
            "n2n3" : [0, 0], # neck2 > neck3
            "n3h" : [0, 0], # neck3 > head
            "hj" : [0, 0], # head > jaw
            "b1b2" : [0, 0], # body1 > body2
            "b2b3" : [0, 0], # body2 > body3
            "b3b4" : [0, 0], # body3 > body4
            "b4b5" : [0, 0], # body4 > body5
            "b5t" : [0, 0],  # body5 > tail  
            "n1wL" : 0, # neck1 > wingL
            "n1wR" : 0, # neck1 > wingR
            "n2wL" : 0, # neck2 > wingL
            "n2wR" : 0, # neck2 > wingR
            "n3wL" : 0, # neck3 > wingL
            "n3wR" : 0 # neck3 > wingR
        }  
        self.create_body(color1, color2)

    def create_body(self, color1, color2):
        # body1: base layer of all model
        self.body1 = geometry.Cube(height=1, color=color2, batch = self.snakeBatch)
        self.body1.deform(geometry.projective_scale(Mat4, x_scale = 0.45, y_scale =1.2, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.neck1 = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.neck1.deform(Mat4.from_translation(Vec3(0, 0.5, 0)))
        self.neck1.deform(geometry.projective_scale(Mat4, x_scale = 0.5, y_scale =1.0, z_scale=0.2, taper = 0.1, correction = 0.4)) 

        self.neck2 = geometry.Cube(height=1, color=color2, batch = self.snakeBatch)
        self.neck2.deform(Mat4.from_translation(Vec3(0, 0.75, 0)))
        self.neck2.deform(geometry.projective_scale(Mat4, x_scale = 0.5, y_scale =1.5, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.neck3 = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.neck3.deform(Mat4.from_translation(Vec3(0, 0.3, 0)))
        self.neck3.deform(geometry.projective_scale(Mat4, x_scale = 0.5, y_scale=0.7, z_scale=0.2, taper = 0.05, correction = 0.3))
        
        self.head = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.head.deform(Mat4.from_translation(Vec3(0, 0.2, 0)))
        self.head.deform(geometry.projective_scale(Mat4, x_scale = 0.4, y_scale =0.6, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.jaw = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.jaw.deform(Mat4.from_translation(Vec3(0, 0.15, 0)))
        self.jaw.deform(geometry.projective_scale(Mat4, x_scale = 0.3, y_scale =0.5, z_scale=0.1, taper = 0.1, correction = 0.4))
        
        #wings are linked to necks
        self.wing1L = geometry.Tripillar(width=-0.75, height=-1, depth=0.1, color=color1, batch = self.snakeBatch)
        self.wing1L.deform(Mat4.from_translation(Vec3(0, 0, 0)))
        self.wing1R = geometry.Tripillar(width=0.75, height=-1, depth=0.1, color=color1, batch = self.snakeBatch)
        self.wing1R.deform(Mat4.from_translation(Vec3(0, 0, 0)))

        self.wing2L = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.wing2L.deform(Mat4.from_translation(Vec3(-0.4, 0, 0)))
        self.wing2L.deform(geometry.projective_scale(Mat4, x_scale = 0.8, y_scale=1.6, z_scale=0.1, taper=-0.01, correction=-0.3))

        self.wing2R = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.wing2R.deform(Mat4.from_translation(Vec3(0.4, 0, 0)))
        self.wing2R.deform(geometry.projective_scale(Mat4, x_scale = 0.8, y_scale=1.6, z_scale=0.1, taper=-0.01, correction=-0.3))

        self.wing3L = geometry.Tripillar(width=-0.88, height=0.8, depth=0.1, color=color1, batch = self.snakeBatch)
        self.wing3L.deform(Mat4.from_translation(Vec3(0, 0, 0)))
        self.wing3R = geometry.Tripillar(width=0.88, height=0.8, depth=0.1, color=color1, batch = self.snakeBatch)
        self.wing3R.deform(Mat4.from_translation(Vec3(0, 0, 0)))

        # body2 is linked to body1 
        self.body2 = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.body2.deform(Mat4.from_translation(Vec3(0, -0.5, 0)))
        self.body2.deform(geometry.projective_scale(Mat4, x_scale = 0.4, y_scale =1.2, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.body3 = geometry.Cube(height=1, color=color2, batch = self.snakeBatch)
        self.body3.deform(Mat4.from_translation(Vec3(0, -0.5, 0)))
        self.body3.deform(geometry.projective_scale(Mat4, x_scale = 0.35, y_scale =1.2, z_scale=0.2, taper = 0.1, correction = 0.4))      

        self.body4 = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.body4.deform(Mat4.from_translation(Vec3(0, -0.5, 0)))
        self.body4.deform(geometry.projective_scale(Mat4, x_scale = 0.3, y_scale =1.2, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.body5 = geometry.Cube(height=1, color=color2, batch = self.snakeBatch)
        self.body5.deform(Mat4.from_translation(Vec3(0, -0.5, 0)))
        self.body5.deform(geometry.projective_scale(Mat4, x_scale = 0.25, y_scale =1.2, z_scale=0.2, taper = 0.1, correction = 0.4))
        
        self.tail = geometry.Cube(height=1, color=color1, batch = self.snakeBatch)
        self.tail.deform(Mat4.from_translation(Vec3(0, -0.3, 0)))
        self.tail.deform(geometry.projective_scale(Mat4, x_scale = 0.15, y_scale =1.2, z_scale=0.1, taper = -0.5, correction = -0.9))
        
        self.set_orientation(self.default_angles)

    def set_orientation(self, angles):
        self.body1.movement = Mat4()
        self.body1.move(Mat4.from_rotation(angle = 0.5*pi, vector=Vec3(0, 0, 1)))
        self.body1.move(angles["wb1"])

        self.neck1.movement = Mat4()
        self.neck1.move(Mat4.from_rotation(angle=angles["b1n1"][0], vector=Vec3(1, 0, 0)))
        self.neck1.move(Mat4.from_rotation(angle=angles["b1n1"][1], vector=Vec3(0, 0, 1)))
        self.neck1.move(Mat4.from_translation(Vec3(0, 0.5, 0)))
        self.neck1.move(self.body1.movement)

        self.neck2.movement = Mat4()
        self.neck2.move(Mat4.from_rotation(angle=angles["n1n2"][0], vector=Vec3(1, 0, 0)))
        self.neck2.move(Mat4.from_rotation(angle=angles["n1n2"][1], vector=Vec3(0, 0, 1)))
        self.neck2.move(Mat4.from_translation(Vec3(0, 1, 0)))
        self.neck2.move(self.neck1.movement)

        self.neck3.movement = Mat4()
        self.neck3.move(Mat4.from_rotation(angle=angles["n2n3"][0], vector=Vec3(1, 0, 0)))
        self.neck3.move(Mat4.from_rotation(angle=angles["n2n3"][1], vector=Vec3(0, 0, 1)))
        self.neck3.move(Mat4.from_translation(Vec3(0, 1.5, 0)))
        self.neck3.move(self.neck2.movement)
        
        self.head.movement = Mat4()
        self.head.move(Mat4.from_rotation(angle=angles["n3h"][0], vector=Vec3(1, 0, 0)))
        self.head.move(Mat4.from_rotation(angle=angles["n3h"][1], vector=Vec3(0, 0, 1)))
        self.head.move(Mat4.from_translation(Vec3(0, 0.7, 0)))
        self.head.move(self.neck3.movement)
        
        self.jaw.movement = Mat4()
        self.jaw.move(Mat4.from_rotation(angle=angles["hj"][0], vector=Vec3(1, 0, 0)))
        self.jaw.move(Mat4.from_rotation(angle=angles["hj"][1], vector=Vec3(0, 0, 1)))
        self.jaw.move(Mat4.from_translation(Vec3(0, 0, -0.2)))
        self.jaw.move(self.head.movement)

        self.wing1L.movement = Mat4()
        self.wing1L.move(Mat4.from_rotation(angle=angles["n1wL"], vector = Vec3(0, 1, -0.3)))
        self.wing1L.move(Mat4.from_translation(Vec3(-0.2, 1, 0)))
        self.wing1L.move(self.neck1.movement)

        self.wing1R.movement = Mat4()
        self.wing1R.move(Mat4.from_rotation(angle=angles["n1wR"], vector = Vec3(0, -1, 0.3)))
        self.wing1R.move(Mat4.from_translation(Vec3(0.2, 1, 0)))
        self.wing1R.move(self.neck1.movement)

        self.wing2L.movement = Mat4()
        self.wing2L.move(Mat4.from_rotation(angle=angles["n2wL"], vector = Vec3(0, 1, 0)))
        self.wing2L.move(Mat4.from_translation(Vec3(-0.2, 0.65, 0)))
        self.wing2L.move(self.neck2.movement)

        self.wing2R.movement = Mat4()
        self.wing2R.move(Mat4.from_rotation(angle=angles["n2wR"], vector = Vec3(0, -1, 0)))
        self.wing2R.move(Mat4.from_translation(Vec3(0.2, 0.65, 0)))
        self.wing2R.move(self.neck2.movement)

        self.wing3L.movement = Mat4()
        self.wing3L.move(Mat4.from_rotation(angle=angles["n3wL"], vector = Vec3(0, 1, 0.4)))
        self.wing3L.move(Mat4.from_translation(Vec3(-0.2, 0, 0)))
        self.wing3L.move(self.neck3.movement)

        self.wing3R.movement = Mat4()
        self.wing3R.move(Mat4.from_rotation(angle=angles["n3wR"], vector = Vec3(0, -1, -0.4)))
        self.wing3R.move(Mat4.from_translation(Vec3(0.2, 0, 0)))
        self.wing3R.move(self.neck3.movement)        
        
        self.body2.movement = Mat4()
        self.body2.move(Mat4.from_rotation(angle=angles["b1b2"][0], vector=Vec3(1, 0, 0)))
        self.body2.move(Mat4.from_rotation(angle=angles["b1b2"][1], vector=Vec3(0, 0, 1)))
        self.body2.move(Mat4.from_translation(Vec3(0, -0.7, 0)))
        self.body2.move(self.body1.movement)
        
        self.body3.movement = Mat4()
        self.body3.move(Mat4.from_rotation(angle=angles["b2b3"][0], vector=Vec3(1, 0, 0)))
        self.body3.move(Mat4.from_rotation(angle=angles["b2b3"][1], vector=Vec3(0, 0, 1)))
        self.body3.move(Mat4.from_translation(Vec3(0, -1.2, 0)))
        self.body3.move(self.body2.movement)
        
        self.body4.movement = Mat4()
        self.body4.move(Mat4.from_rotation(angle=angles["b3b4"][0], vector=Vec3(1, 0, 0)))
        self.body4.move(Mat4.from_rotation(angle=angles["b3b4"][1], vector=Vec3(0, 0, 1)))
        self.body4.move(Mat4.from_translation(Vec3(0, -1.2, 0)))
        self.body4.move(self.body3.movement)
        
        self.body5.movement = Mat4()
        self.body5.move(Mat4.from_rotation(angle=angles["b4b5"][0], vector=Vec3(1, 0, 0)))
        self.body5.move(Mat4.from_rotation(angle=angles["b4b5"][1], vector=Vec3(0, 0, 1)))
        self.body5.move(Mat4.from_translation(Vec3(0, -1.2, 0)))
        self.body5.move(self.body4.movement)
        
        self.tail.movement = Mat4()
        self.tail.move(Mat4.from_rotation(angle=angles["b5t"][0], vector=Vec3(1, 0, 0)))
        self.tail.move(Mat4.from_rotation(angle=angles["b5t"][1], vector=Vec3(0, 0, 1)))
        self.tail.move(Mat4.from_translation(Vec3(0, -1.0, 0)))
        self.tail.move(self.body5.movement)