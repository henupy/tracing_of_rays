"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

File contains an abstract Hittable baseclass and classes for spheres
that are in the scene
"""

import math
import vec3

from ray import Ray
from abc import ABC
from typing import Optional
from materials import Material
from collision import Collision

# For typing
num = int | float


class Hittable(ABC):
    def __init__(self, center: vec3.Vec3, radius: num, material: Material) -> None:
        """
        :param center:
        :param radius:
        """
        self.center = center
        self.radius = radius
        self.material = material
        self.collision = None

    def hit(self, ray: Ray, t_min: num, t_max: num) -> bool:
        """
        Determines if the ray hits the sphere
        :param ray:
        :param t_min:
        :param t_max:
        :return:
        """


class Sphere(Hittable):
    def __init__(self, center: vec3.Vec3, radius: num, material: Material) -> None:
        """
        :param center: Location of the sphere's center
        :param radius: Radius of the sphere
        :param material: Material of the sphere
        """
        super().__init__(center, radius, material)
        self.collision = None

    def hit(self, ray: Ray, t_min: num, t_max: num) -> bool:
        """
        Determines if the ray hits the sphere
        :param ray:
        :param t_min:
        :param t_max:
        :return:
        """
        oc = ray.origin - self.center
        a = ray.direction.length_squared()
        half_b = vec3.dot(oc, ray.direction)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False

        # Find the nearest root that lies in the acceptable range
        sqrtd = math.sqrt(discriminant)
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False
        t = root
        pos = ray.step(t)
        norm = (pos - self.center) / self.radius
        c = Collision(pos, norm, t, self.material)
        c.set_face_normal(ray, norm)
        self.collision = c
        return True


class HittableList:
    """
    Keeps track of the hittable objects
    """
    def __init__(self) -> None:
        self._objects: list[Hittable] = []

    def add(self, obj: Hittable) -> None:
        """
        Adds a hittable object into the list
        :param obj:
        :return:
        """
        self._objects.append(obj)

    def hit(self, ray: Ray, t_min: num, t_max: num) -> Optional[Collision]:
        """
        Checks if the ray hits any of the objects in the list
        :param ray:
        :param t_min:
        :param t_max:
        :return:
        """
        closest_obj = None
        for obj in self._objects:
            if obj.hit(ray, t_min, t_max):
                t_max = obj.collision.t
                closest_obj = obj

        if closest_obj is not None:
            return closest_obj.collision
        return None
