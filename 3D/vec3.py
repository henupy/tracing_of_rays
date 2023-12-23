"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

File for a 3D vector object
"""

from __future__ import annotations

import math
import random

# For typing
num = int | float


class Vec3:
    """
    Contains the basic operations for a 3D vector
    """
    def __init__(self, x: num, y: num, z: num) -> None:
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param z: z-coordinate
        """
        self.x = x
        self.y = y
        self.z = z

    def length_squared(self) -> num:
        """
        :return:
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> num:
        """
        :return:
        """
        return math.sqrt(self.length_squared())

    def near_zero(self, eps: num = 1e-8) -> bool:
        """
        Check if the vector is very close to zero in all dimensions
        :param eps: Value for epsilon (default 1e-8)
        :return:
        """
        return abs(self.x) < eps and abs(self.y) < eps and abs(self.z) < eps

    def __neg__(self) -> Vec3:
        """
        :return:
        """
        return self * -1

    def __iadd__(self, other: Vec3) -> Vec3:
        """
        :param other:
        :return:
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __add__(self, other: Vec3) -> Vec3:
        """
        Addition of two vectors
        :param other:
        :return:
        """
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x, y, z)

    def __sub__(self, other: Vec3) -> Vec3:
        """
        Substraction of two vectors
        :param other:
        :return:
        """
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x, y, z)

    def __mul__(self, other: num | Vec3) -> Vec3:
        """
        Elementwise multiplication of either one vector with a scalar,
        or of two vectors
        :param other:
        :return:
        """
        if isinstance(other, Vec3):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vec3(x, y, z)

    def __truediv__(self, div: num) -> Vec3:
        """
        Division of a vector with a numeric divisor
        :param div:
        :return:
        """
        return self * (1 / div)

    def __str__(self) -> str:
        """
        :return:
        """
        return f"x={self.x}, y={self.y}, z={self.z}"


# Some useful functions

def rand_range(a: num, b: num) -> num:
    """
    Returns a random number in the range [a, b)
    :param a:
    :param b:
    :return:
    """
    return a + random.random() * (b - a)


def dot(u: Vec3, v: Vec3) -> num:
    """
    Dot product of two vectors
    :param u:
    :param v:
    :return:
    """
    return u.x * v.x + u.y * v.y + u.z * v.z


def cross(u: Vec3, v: Vec3) -> Vec3:
    """
    Cross product of two vectors
    :param u:
    :param v:
    :return:
    """
    x = u.y * v.z - u.z * v.y
    y = u.z * v.x - u.x * v.z
    z = u.x * v.y - u.y * v.x
    return Vec3(x, y, z)


def unit_vector(u: Vec3) -> Vec3:
    """
    :return:
    """
    return u / u.length()


def random_in_unit_sphere() -> Vec3:
    """
    Returns a random point that is inside a unit sphere
    :return:
    """
    while True:
        p = Vec3(random.random(), random.random(), random.random())
        if p.length_squared() < 1:
            return p


def random_unit_vector() -> Vec3:
    """
    Returns a random unit vector
    :return:
    """
    return unit_vector(random_in_unit_sphere())


def random_in_hemisphere(normal: Vec3) -> Vec3:
    """
    Returns a vector that is in the same hemisphere as the given normal
    :param normal:
    :return:
    """
    in_unit_sphere = random_in_unit_sphere()
    if dot(in_unit_sphere, normal) > 0:
        return in_unit_sphere
    else:
        return -in_unit_sphere


def random_in_unit_disk() -> Vec3:
    """
    Returns a random vector originating from a disk
    :return:
    """
    while True:
        p = Vec3(rand_range(-1, 1), rand_range(-1, 1), 0)
        if p.length_squared() < 1:
            return p


def rand_vect() -> Vec3:
    """
    Returns a random vector
    :return:
    """
    return Vec3(random.random(), random.random(), random.random())


def rand_range_vect(mini: num, maxi: num) -> Vec3:
    """
    :param mini:
    :param maxi:
    :return:
    """
    return Vec3(rand_range(mini, maxi), rand_range(mini, maxi), rand_range(mini, maxi))


def reflect(v: Vec3, n: Vec3) -> Vec3:
    """
    Reflection of vector v from a surface with a normal vector n
    :param v:
    :param n:
    :return:
    """
    return v - n * dot(v, n) * 2


def refract(uv: Vec3, n: Vec3, ir: num) -> Vec3:
    """
    Refraction
    :param uv:
    :param n:
    :param ir:
    :return:
    """
    cos_theta = min(dot(-uv, n), 1)
    r_out_perp = (uv + n * cos_theta) * ir
    r_out_parallel = n * -math.sqrt(abs(1 - r_out_perp.length_squared()))
    return r_out_perp + r_out_parallel
