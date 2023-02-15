"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

A camera object that generates the ray
"""

import math
import vec3

from ray import Ray

# For typing
num = int | float


class Camera:
    def __init__(self, lookfrom: vec3.Vec3, lookat: vec3.Vec3, vup: vec3.Vec3,
                 vfov: num, aspect_ratio: num, aperture: num, focus_dist: num) -> None:
        """
        :param lookfrom:
        :param lookat:
        :param vup:
        :param vfov: Vertical field of view in degrees
        :param aspect_ratio: Aspect ratio of the image
        :param aperture:
        :param focus_dist:
        """
        theta = self._deg2rad(vfov)
        h = math.tan(theta / 2)
        viewport_h = 2 * h
        viewport_w = aspect_ratio * viewport_h
        w = vec3.unit_vector(lookfrom - lookat)
        self.u = vec3.unit_vector(vec3.cross(vup, w))
        self.v = vec3.cross(w, self.u)
        self.origin = lookfrom
        self.hor = self.u * viewport_w * focus_dist
        self.ver = self.v * viewport_h * focus_dist
        wf = w * focus_dist
        self.lower_left_corner = self.origin - self.hor / 2 - self.ver / 2 - wf
        self.lens_radius = aperture / 2

    def get_ray(self, s: num, t: num) -> Ray:
        """
        :param s:
        :param t:
        :return:
        """
        rd = vec3.random_in_unit_disk() * self.lens_radius
        offset = self.u * rd.x + self.v * rd.y
        return Ray(
            self.origin + offset,
            self.lower_left_corner + self.hor * s + self.ver * t - self.origin - offset
        )

    @staticmethod
    def _deg2rad(degs: num) -> num:
        """
        Conversion of degrees to radians
        :return:
        """
        return degs * math. pi / 180
