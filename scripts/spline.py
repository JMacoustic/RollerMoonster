import numpy as np
import sympy as sp
from math import sqrt
from utils import normalize, np2sp, integrate


x = sp.symbols('x')

def Bezier1D(cp0, cp1, cp2, cp3):
    basis_mat = np.array([[1, -3, 3, -1],
                        [0, 3, -6, 3],
                        [0, 0, 3, -3],
                        [0, 0, 0, 1]])
    cp_mat = np.transpose(np.vstack([cp0, cp1, cp2, cp3]))
    poly_mat = cp_mat @ basis_mat
    
    polynomial = np.polynomial.Polynomial(poly_mat[0].tolist())
    return polynomial


class NatCubeSpline:
    def __init__(self, points): # frame smoothness: 0~100
        self.pass_points = points
        self.point_T = np.transpose(points)
        self.N = points.shape[0]
        self.dim = points.shape[1]
        self.umax = self.N-1
        self.umin = 0
        self.du = 0
        self.closed = np.array_equal(points[0], points[-1])
        self.hmax = max(self.point_T[2])
        self.set_control_points()
        self.set_hmax(div=1000)
    
    def limit_u(self, u):
        return (u - self.umin) % (self.umax - self.umin) + self.umin

    def set_control_points(self):
        N = self.N
        dim = self.dim
        A = np.zeros((2*N - 2, 2*N - 2))
        B = np.zeros((2*N - 2, dim)) 

        for i in range(N - 2):
            # Tangency constraint
            A[i][2*i + 1] = 1
            A[i][2*(i + 1)] = 1
            B[i] = 2 * self.point_T[:, i+1] 

            # Curvature constraint
            A[i + N - 2][2*i] = 1
            A[i + N - 2][2*i + 1] = -2
            A[i + N - 2][2*(i + 1)] = 2
            A[i + N - 2][2*(i + 1)+1] = -1 

        # extra 2 more constraints
        if self.closed:
            A[2*N - 4][0] = 1
            A[2*N - 4][-1] = 1
            B[2*N - 4] = 2 * self.point_T[:, 0]

            A[2*N - 3][-2] = 1
            A[2*N - 3][-1] = -2
            A[2*N - 3][0] = 2
            A[2*N - 3][1] = -1
        else:
            A[2*N - 4][0] = -2
            A[2*N - 4][1] = 1
            B[2*N - 4] = -self.point_T[:, 0]

            A[2*N - 3][-2] = 1
            A[2*N - 3][-1] = -2
            B[2*N - 3] = -self.point_T[:, -1]

        control_points = np.stack([np.linalg.solve(A, B[:, d]) for d in range(dim)], axis=-1)
        self.control_points = control_points.reshape(-1, 2, dim)
        self.generate_bezier()

    def generate_bezier(self):
        self.curve_list = []
        self.sp_curve_list = []
        
        for d in range(self.dim):
            segments = []
            sp_segments= []
            for i in range(self.N-1):
                curve = Bezier1D(self.pass_points[i][d], self.control_points[i][0][d], self.control_points[i][1][d], self.pass_points[i+1][d])
                segments.append(curve)
                sp_segments.append(np2sp(curve))
            self.curve_list.append(segments)
            self.sp_curve_list.append(sp_segments)
        self.setup_differentials()

    def setup_differentials(self):
        self.ds_list = []    
        self.cumulative_lengths = [0.0]

        for i in range(self.N - 1):
            ds_expr = sp.sqrt(sp.diff(self.sp_curve_list[0][i])**2 +
                            sp.diff(self.sp_curve_list[1][i])**2 +
                            sp.diff(self.sp_curve_list[2][i])**2)
            ds_func = sp.lambdify(x, ds_expr, 'numpy') 

            total = self.cumulative_lengths[-1] + integrate(ds_func, 0, 1, n_intervals=10)
            self.cumulative_lengths.append(total)
            self.ds_list.append(ds_func)
    
    # reparametrize the whole spline in single parameter, u
    # u is same scale as t: if there are N points and N-1 segments, 0 <= u <= N-1 
    def coordinate(self, u):
        u = self.limit_u(u)

        n_segments = self.N-1
        if u <= 0:
            seg = 0
            t = 0.0
        elif u >= n_segments:
            seg = n_segments-1
            t = 1.0
        else:
            seg = int(u)
            t = u-seg

        point = [self.curve_list[d][seg](t) for d in range(self.dim)]
        return np.array(point)

    def tangent(self, u):
        u = self.limit_u(u)

        n_segments = self.N-1
        if u <= 0:
            seg = 0
            t = 0.0
        elif u >= n_segments:
            seg = n_segments-1
            t = 1.0
        else:
            seg = int(u)
            t = u-seg

        tangent = [self.curve_list[d][seg].deriv()(t) for d in range(self.dim)]
        return np.array(tangent)
    
    def normal(self, u):
        u = self.limit_u(u)

        n_segments = self.N-1
        if u <= 0:
            seg = 0
            t = 0.0
        elif u >= n_segments:
            seg = n_segments-1
            t = 1.0
        else:
            seg = int(u)
            t = u-seg

        normal = [self.curve_list[d][seg].deriv().deriv()(t) for d in range(self.dim)]
        return np.array(normal)
    
    def binormal(self, u):
        u = self.limit_u(u)

        binormal = np.cross(self.tangent(u), self.normal(u))
        return np.array(binormal)
    
    # frenet frame with modification. allows smoothing factor du
    def frenet_frame(self, u):
        u = self.limit_u(u)

        z = normalize(self.tangent(u))
        y = normalize(self.binormal(u-self.du))
        x = normalize(np.cross(y, z))

        frame = np.vstack((x, y, z))
        return frame
    
    # frame that keeps y axis towards V_up vector
    def up_frame(self, u, V_up = np.array([0, 0, 1])):
        u = self.limit_u(u)

        z = normalize(self.tangent(u))
        x = normalize(np.cross(V_up, z))
        y = normalize(np.cross(z, x))

        frame = np.vstack((x, y, z))
        return frame

    def length(self, u):        
        seg = int(u)
        fraction = u - seg
        length = self.cumulative_lengths[seg]

        if fraction > 0:
            ds = self.ds_list[seg]
            length += integrate(ds, 0, fraction, n_intervals=10)
        
        return length
    
    def inv_length(self, s):
        u0 = self.umax/2
        u = u0
        error = abs(self.length(u0) - s)
        threshold = 0.01
        iteration = 0
        max_iter = 1000
        
        while iteration <= max_iter:
            seg = int(u)
            current_length = self.length(u)
            error = s - current_length
            dlength = - self.ds_list[seg](u)

            # print(f"iter: {iteration}, u: {u}, s(current): {current_length}, error: {error}")
            if (abs(error) <= threshold) or (dlength == 0): break

            u = u - (s-current_length)/dlength
            if u >= self.umax or u<= self.umin:
                u = self.umin
                break

            iteration += 1

        return u
    
    def speed(self, u, g=9.8):
        #u =self.limit_u(u)
        hmax = self.hmax
        h = self.coordinate(u)[2]
        if hmax < h:
            Warning("h bigger than hmax. simulation error")
        speed = sqrt(2*g*(hmax-h))
        return speed
    
    def set_hmax(self, div):
        du = self.umax/div

        for i in range(div):
            z = self.coordinate(i*du)[2]
            if z > self.hmax:
                self.hmax = z
        self.hmax +=0.05
