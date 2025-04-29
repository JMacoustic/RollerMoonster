from spline import NatCubeSpline
import numpy as np
import utils
import matplotlib.pyplot as plt

test_counter = utils.TimeCounter(0)

test_points = np.array([
    [0, 0, 0],
    [1, 1, 0],
    [2, 3, 0],
    [1, 3, 5],
    [1, 2, 5],
    [4, 1, 5],
    [4.5, 2, 0],
    [3, 6, 0],
    [0, 1, 0],
    [0, 0, 0]
])

test = NatCubeSpline(points=test_points)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d')

# Plot original points
ax.plot(*test_points.T, 'o--', label='Given Points')

# Plot spline using global parameter u
u_vals = np.linspace(test.umin, test.umax, 300)
spline_coords = np.array([test.coordinate(u) for u in u_vals])
ax.plot(spline_coords[:, 0], spline_coords[:, 1], spline_coords[:, 2], 'r', label='Spline Curve')

# Setup axis
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_zlim(-1, 6)
ax.set_title("Roller coaster simulation")
ax.legend()

# Initialize parameters
tmax = 100
smax = test.length(test.umax)
u = 0
s = 0
t = 0
dt = 0.01

# Plot moving orientation
frame_quivers = []

while t<tmax:
    # Update s, t, u
    if s >= smax:
        s = 0
    s += test.speed(u) * dt
    t += dt
    u = test.inv_length(s)

    # Clear previous quivers
    for quiver in frame_quivers:
        quiver.remove()
    frame_quivers.clear()

    # Plot new frame
    pt = test.coordinate(u)
    x, y, z = test.up_frame(u)

    frame_quivers.append(ax.quiver(pt[0], pt[1], pt[2], x[0], x[1], x[2], color='r', length=0.5))
    frame_quivers.append(ax.quiver(pt[0], pt[1], pt[2], y[0], y[1], y[2], color='g', length=0.5))
    frame_quivers.append(ax.quiver(pt[0], pt[1], pt[2], z[0], z[1], z[2], color='b', length=0.5))

    plt.pause(dt)

plt.show()