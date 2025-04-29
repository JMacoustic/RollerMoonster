from scripts import geometry
from pyglet.math import Mat4, Vec3
from scripts.utils import centerNvector

class Rail:
    def __init__(self, spline, thickness, width, n_cylinders, n_plates, batch=None, frame="up_frame"):
        self.spline = spline
        self.thickness = thickness
        self.width = width
        self.n_cylinders = n_cylinders
        self.n_plates = n_plates
        self.du = (spline.N-1)/n_cylinders
        self.railbatch = batch
        self.frame = frame
        self.color1 = (1, 0, 0, 0.5)
        self.color2 = (1, 1, 1, 1)
        self.create_rail()

    def create_rail(self):
        self.objects = []
        
        for i in range(self.n_cylinders):
            u = i*self.du
            ds = self.spline.length(u-3*self.du/5)-self.spline.length(u+3*self.du/5)

            if self.frame == "up_frame":
                x, y, z = self.spline.up_frame(u)
            if self.frame == "frenet_frame":
                x, y, z = self.spline.frenet_frame(u)

            left_cylinder = geometry.Cylinder(radius=self.thickness/2.0, height=ds, batch=self.railbatch, color=self.color1)
            left_cylinder.matrix = Mat4.from_translation(0.1*Vec3(*x)) @ centerNvector(Mat4, self.spline.coordinate(u), z, y)

            right_cylinder = geometry.Cylinder(radius=self.thickness/2.0, height=ds, batch=self.railbatch, color=self.color1)
            right_cylinder.matrix = Mat4.from_translation(-0.1*Vec3(*x)) @ centerNvector(Mat4, self.spline.coordinate(u), z, y)
            self.objects.append(left_cylinder)
            self.objects.append(right_cylinder)
    
        length = self.spline.length(self.spline.umax)
        dlength = length/self.n_plates

        for i in range(self.n_plates):
            s = dlength*i
            u = self.spline.inv_length(s)

            if self.frame == "up_frame":
                x, y, z = self.spline.up_frame(u)
            if self.frame == "frenet_frame":
                x, y, z = self.spline.frenet_frame(u)
            plate = geometry.Cube(width=0.2, height=0.02, depth=0.1, batch=self.railbatch, color=self.color2)
            plate.matrix = Mat4.from_translation(0.03*Vec3(*y)) @ centerNvector(Mat4, self.spline.coordinate(u), z, y)
            self.objects.append(plate)
    
    def switch_frame(self):
        if self.frame == "up_frame":
            self.frame = "frenet_frame" 
        else:
            self.frame = "up_frame"
        
        for obj in self.objects:
            obj.delete()
        self.create_rail()

class Cart:
    def __init__(self, spline, frame="up_frame", batch=None):
        self.spline = spline
        self.frame = frame
        self.color = (0.2, 0.2, 0.2, 0.2)
        self.cartBatch = batch
        self.create_cart()
        
    def create_cart(self):
        self.cart = geometry.Cube(width= 0.1, height=0.2, depth= 0.4, batch=self.cartBatch, color=self.color)
        if self.frame == "up_frame":
            x, y, z = self.spline.up_frame(0)
        if self.frame == "frenet_frame":
            x, y, z = self.spline.frenet_frame(0)
        self.cart.matrix = Mat4.from_translation(0.05*Vec3(*y)) @ centerNvector(Mat4, self.spline.coordinate(0), z, x)
        
    def move(self, u):
        if self.frame == "up_frame":
            x, y, z = self.spline.up_frame(u)
        if self.frame == "frenet_frame":
            x, y, z = self.spline.frenet_frame(u)
        self.cart.matrix = Mat4.from_translation(0.05*Vec3(*y)) @ centerNvector(Mat4, self.spline.coordinate(u), z, x)
    
    def switch_frame(self): 
        if self.frame == "up_frame":
            self.frame = "frenet_frame" 
        else:
            self.frame = "up_frame"
        self.cart.delete()
        self.create_cart()    
