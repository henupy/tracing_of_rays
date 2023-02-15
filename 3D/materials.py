"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

Contains an abstract Material class and classes for some materials
"""
import math
import random

import vec3

from ray import Ray
from typing import Optional

# For typing
num = int | float


class Material:
    def __init__(self, albedo: vec3.Vec3, fuzz: num = 0) -> None:
        """
        :param albedo:
        :param fuzz:
        """
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, ray_in: Ray, pos: vec3.Vec3, norm: vec3.Vec3,
                front_face: bool) -> Optional[tuple[Ray, vec3.Vec3]]:
        """
        :param ray_in:
        :param pos:
        :param norm:
        :param front_face:
        :return:
        """


class Lambertian(Material):
    def __init__(self, albedo: vec3.Vec3, fuzz: num = 0) -> None:
        """
        :param albedo:
        """
        super().__init__(albedo, fuzz)

    def scatter(self, ray_in: Ray, pos: vec3.Vec3, norm: vec3.Vec3,
                front_face: bool) -> Optional[tuple[Ray, vec3.Vec3]]:
        """
        :param ray_in:
        :param pos:
        :param norm:
        :param front_face:
        :return:
        """
        scatter_direction = norm + vec3.random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = norm
        scattered = Ray(pos, scatter_direction)
        return scattered, self.albedo


class Metal(Material):
    def __init__(self, albedo: vec3.Vec3, fuzz: num = 0) -> None:
        """
        :param albedo:
        """
        super().__init__(albedo, fuzz)

    def scatter(self, ray_in: Ray, pos: vec3.Vec3, norm: vec3.Vec3,
                front_face: bool) -> Optional[tuple[Ray, vec3.Vec3]]:
        """
        :param ray_in:
        :param pos:
        :param norm:
        :param front_face:
        :return:
        """
        r_dir = vec3.unit_vector(ray_in.direction)
        reflected = vec3.reflect(r_dir, norm)
        scattered = Ray(pos, reflected + vec3.random_in_unit_sphere() * self.fuzz)
        if vec3.dot(scattered.direction, norm) > 0:
            return scattered, self.albedo
        return None


class Dielectric(Material):
    def __init__(self, ir: num) -> None:
        super().__init__(vec3.Vec3(0, 0, 0))
        self.ir = ir

    def scatter(self, ray_in: Ray, pos: vec3.Vec3, norm: vec3.Vec3,
                front_face: bool) -> Optional[tuple[Ray, vec3.Vec3]]:
        """
        :param ray_in:
        :param pos:
        :param norm:
        :param front_face:
        :return:
        """
        attenuation = vec3.Vec3(1, 1, 1)
        if front_face:
            ir = 1 / self.ir
        else:
            ir = self.ir
        unit_dir = vec3.unit_vector(ray_in.direction)
        cos_theta = min(vec3.dot(-unit_dir, norm), 1)
        sin_theta = math.sqrt(1 - cos_theta * cos_theta)
        cannot_refract = ir * sin_theta > 1
        if cannot_refract or self._reflectance(cos_theta, ir) > random.random():
            direction = vec3.reflect(unit_dir, norm)
        else:
            direction = vec3.refract(unit_dir, norm, ir)
        scattered = Ray(pos, direction)
        return scattered, attenuation

    @staticmethod
    def _reflectance(cos_theta: num, ir: num) -> num:
        """
        Reflectance with Schlick's approximation
        :param cos_theta:
        :param ir:
        :return:
        """
        r0 = (1 - ir) / (1 + ir)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow((1 - cos_theta), 5)
