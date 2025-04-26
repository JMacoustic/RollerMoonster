from __future__ import annotations
from pyglet.math import Mat4, Mat3, Vec3
from math import sqrt
import typing as _typing

class newQuaternion(_typing.NamedTuple):
    """Quaternion."""

    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_mat3(cls, mat: Mat3):
        m00, m01, m02 = mat.a, mat.b, mat.c
        m10, m11, m12 = mat.d, mat.e, mat.f
        m20, m21, m22 = mat.g, mat.h, mat.i

        trace = m00 + m11 + m22

        if trace > 0.0:
            s = (trace + 1.0) ** 0.5
            w = 0.5 * s
            s = 0.5 / s
            x = (m21 - m12) * s
            y = (m02 - m20) * s
            z = (m10 - m01) * s
        else:
            if m00 > m11 and m00 > m22:
                s = (1.0 + m00 - m11 - m22) ** 0.5
                x = 0.5 * s
                s = 0.5 / s
                y = (m01 + m10) * s
                z = (m02 + m20) * s
                w = (m21 - m12) * s
            elif m11 > m22:
                s = (1.0 + m11 - m00 - m22) ** 0.5
                y = 0.5 * s
                s = 0.5 / s
                x = (m01 + m10) * s
                z = (m12 + m21) * s
                w = (m02 - m20) * s
            else:
                s = (1.0 + m22 - m00 - m11) ** 0.5
                z = 0.5 * s
                s = 0.5 / s
                x = (m02 + m20) * s
                y = (m12 + m21) * s
                w = (m10 - m01) * s

        return cls(w, x, y, z)

    @classmethod
    def from_mat4(cls) -> newQuaternion:
        raise NotImplementedError

    def to_mat4(self) -> Mat4:
        w = self.w
        x = self.x
        y = self.y
        z = self.z

        a = 1 - (y**2 + z**2) * 2
        b = 2 * (x * y - z * w)
        c = 2 * (x * z + y * w)

        e = 2 * (x * y + z * w)
        f = 1 - (x**2 + z**2) * 2
        g = 2 * (y * z - x * w)

        i = 2 * (x * z - y * w)
        j = 2 * (y * z + x * w)
        k = 1 - (x**2 + y**2) * 2

        # a, b, c, -
        # e, f, g, -
        # i, j, k, -
        # -, -, -, -

        return Mat4(a, b, c, 0.0, e, f, g, 0.0, i, j, k, 0.0, 0.0, 0.0, 0.0, 1.0)

    def to_mat3(self) -> Mat3:
        w = self.w
        x = self.x
        y = self.y
        z = self.z

        a = 1 - (y**2 + z**2) * 2
        b = 2 * (x * y - z * w)
        c = 2 * (x * z + y * w)

        e = 2 * (x * y + z * w)
        f = 1 - (x**2 + z**2) * 2
        g = 2 * (y * z - x * w)

        i = 2 * (x * z - y * w)
        j = 2 * (y * z + x * w)
        k = 1 - (x**2 + y**2) * 2

        # a, b, c, -
        # e, f, g, -
        # i, j, k, -
        # -, -, -, -

        return Mat3(*(a, b, c, e, f, g, i, j, k))

    def length(self) -> float:
        """Calculate the length of the Quaternion.

        The distance between the coordinates and the origin.
        """
        return sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def conjugate(self) -> newQuaternion:
        return newQuaternion(self.w, -self.x, -self.y, -self.z)

    def dot(self, other: newQuaternion) -> float:
        a, b, c, d = self
        e, f, g, h = other
        return a * e + b * f + c * g + d * h

    def normalize(self) -> newQuaternion:
        m = self.length()
        if m == 0:
            return self
        return newQuaternion(self.w / m, self.x / m, self.y / m, self.z / m)

    def __add__(self, other: newQuaternion) -> newQuaternion:
        a, b, c, d = self
        e, f, g, h = other
        return newQuaternion(a + e, b + f, c + g, d + h)

    def __sub__(self, other: newQuaternion) -> newQuaternion:
        a, b, c, d = self
        e, f, g, h = other
        return newQuaternion(a - e, b - f, c - g, d - h)

    def __mul__(self, scalar: float) -> newQuaternion:
        w, x = self.w * scalar, self.x * scalar
        y, z = self.y * scalar, self.z * scalar
        return newQuaternion(w, x, y, z)

    def __truediv__(self, other: newQuaternion) -> newQuaternion:
        return ~self @ other

    def __invert__(self) -> newQuaternion:
        return self.conjugate() * (1 / self.dot(self))

    def __matmul__(self, other: newQuaternion) -> newQuaternion:
        a, u = self.w, Vec3(*self[1:])
        b, v = other.w, Vec3(*other[1:])
        scalar = a * b - u.dot(v)
        vector = v * a + u * b + u.cross(v)
        return newQuaternion(scalar, *vector)