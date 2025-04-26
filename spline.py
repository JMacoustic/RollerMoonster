import numpy as np

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
    def __init__(self, points):
        self.pass_points = points
        self.point_T = np.transpose(points)
        self.N = points.shape[0]
        self.dim = points.shape[1]
        self.closed = np.array_equal(points[0], points[-1])
        self.set_control_points()

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
        for d in range(self.dim):
            segments = []
            for i in range(self.N-1):
                curve = Bezier1D(self.pass_points[i][d], self.control_points[i][0][d], self.control_points[i][1][d], self.pass_points[i+1][d])
                segments.append(curve)
            self.curve_list.append(segments)
    
    def coordinate(self, u):
        n_segments = self.N-1
        seg_length = 1.0/n_segments
        if u <= 0:
            seg = 0
            t = 0.0
        elif u >= 1:
            seg = n_segments-1
            t = 1.0
        else:
            seg = int(u*n_segments)
            t = (u-seg*seg_length) / seg_length

        point = [self.curve_list[d][seg](t) for d in range(self.dim)]
        return np.array(point)

    def tangent(self, u):
        n_segments = self.N-1
        seg_length = 1.0/n_segments
        if u <= 0:
            seg = 0
            t = 0.0
        elif u >= 1:
            seg = n_segments-1
            t = 1.0
        else:
            seg = int(u*n_segments)
            t = (u-seg*seg_length) / seg_length

        tangent = [self.curve_list[d][seg].deriv()(t) / seg_length for d in range(self.dim)]
        return np.array(tangent)