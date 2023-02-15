"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

File contains a class for a Collision, which stores information about
object that the ray hits and where the ray hits the hittable object
"""

import vec3

from ray import Ray
from typing import Optional
from materials import Material

# For typing
num = int | float


class Collision:
    def __init__(self, pos: vec3.Vec3, normal: vec3.Vec3, t: num,
                 material: Material) -> None:

        """
        :param pos: Location of the object
        :param normal: The normal vector of the object
        :param t: The point along the ray where the collision occurs
        :param material: The material of the object
        """
        self.pos = pos
        self.normal = normal
        self.t = t
        self.material = material
        self.front_face = True

    def set_face_normal(self, ray: Ray, outward_norm: vec3.Vec3) -> None:
        """
        Sets the face normal correct, i.e., whether it points inwards or outwards
        :param ray:
        :param outward_norm:
        :return:
        """
        self.front_face = vec3.dot(ray.direction, outward_norm) < 0
        if self.front_face:
            self.normal = outward_norm
        else:
            self.normal = -outward_norm

    def interact(self, ray_in: Ray) -> Optional[tuple[Ray, vec3.Vec3]]:
        """
        Interacts with the object according to its material
        :return:
        """
        return self.material.scatter(ray_in, self.pos, self.normal, self.front_face)
