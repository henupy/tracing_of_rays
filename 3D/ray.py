"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

File for a Ray class
"""

import vec3

# For typing
num = int | float


class Ray:
    def __init__(self, origin: vec3.Vec3, direction: vec3.Vec3) -> None:
        """
        :param origin: Origin (location) of the ray
        :param direction: The direction of the ray
        """
        self.origin = origin
        self.direction = direction

    def step(self, t: num) -> vec3.Vec3:
        """
        Moves the tip of the ray vector t steps forward (or backward if t < 0)
        :param t:
        :return:
        """
        return self.origin + self.direction * t
