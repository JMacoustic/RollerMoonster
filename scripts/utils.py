import numpy as np
import sympy as sp
from pyglet.math import Mat4

class TimeCounter:
	def __init__(self, t0):
		self.t = t0
		self.t0 = t0
	def update_time(self, dt):
		self.t += dt
	def print_time(self):
		print("current time: ", self.t)
	def reset(self):
		self.t = self.t0
		
class EventWatcher:
	def __init__(self):
		self.thirdview = False
		self.moving = False

class value:
	def __init__(self, value0):
		self.value0=value0
		self.value=value0
	def reset(self):
		self.value = self.value0
	def add(self, dvalue):
		self.value += dvalue

def normalize(u):
	norm = np.linalg.norm(u)
	if norm == 0: 
		Warning("vector norm is 0. returning 0 vector")
		return u
	return u / norm


def integrate(P, u1, u2, n_intervals=10):
    u1 = float(u1)
    u2 = float(u2)
    n_samples = 2 * n_intervals + 1
    x_vals = np.linspace(u1, u2, n_samples)
    y_vals = P(x_vals)  # Fast vectorized evaluation

    h = (u2 - u1) / (n_samples - 1)

    result = h/3 * (y_vals[0]
                    + 2 * np.sum(y_vals[2:-1:2])
                    + 4 * np.sum(y_vals[1::2])
                    + y_vals[-1])
    
    return result

def np2sp(poly_np, symbol = 'x'):
    x = sp.symbols(symbol)
    expr = sum(coef * x**i for i, coef in enumerate(poly_np.coef))
    return expr

def centerNvector(cls: type[Mat4], center, vector, up) -> Mat4:
    """Create a Mat4 from center of geometry and vector for direction. both numpy array"""
    z = normalize(vector)
    up = normalize(up)
    x = normalize(np.cross(up, z))
    y = normalize(np.cross(z, x))

    return cls(x[0], x[1], x[2], 0,  
               y[0], y[1], y[2], 0,  
               z[0], z[1], z[2], 0,  
               center[0], center[1], center[2], 1)