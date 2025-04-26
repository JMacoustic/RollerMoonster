from spline import NatCubeSpline
import matplotlib.pyplot as plt
import numpy as np

test_points = np.array([
    [0, 0, 0],
    [1, 1, 0],
    [2, 3, 0],
    [1, 3, 1],
    [1, 2, 1],
    [4, 1, 1],
    [4.5, 2, 0],
    [3, 6, 0],
    [0, 1, 0],
    [0, 0, 0]
])
# Instantiate the spline
test = NatCubeSpline(points=test_points)

# Plot spline and tangents
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot original points
ax.plot(*test_points.T, 'o--', label='Given Points')

# Plot spline using global parameter u
u_vals = np.linspace(0, 1, 100)
spline_coords = np.array([test.coordinate(u) for u in u_vals])
ax.plot(spline_coords[:, 0], spline_coords[:, 1], spline_coords[:, 2], 'r', label='Spline Curve')

# Plot tangent vectors
u_samples = np.linspace(0, 1, 10)
for u in u_samples:
    pt = test.coordinate(u)
    tan = test.tangent(u)
    tan = tan / np.linalg.norm(tan) * 0.5
    ax.quiver(pt[0], pt[1], pt[2], tan[0], tan[1], tan[2], color='g', length=0.5, normalize=True)

ax.set_title("3D Natural Cubic Bézier Spline with Tangents")
ax.legend()
plt.show()