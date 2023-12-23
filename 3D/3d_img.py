"""
Raytracing in 3D

Follows the Raytracing in One Weekend book:
https://raytracing.github.io/

Mainfile, generates the raytraced images
"""

import math
import vec3
import random

from ray import Ray
from camera import Camera
from timeit import default_timer
from hittables import HittableList, Sphere
from materials import Lambertian, Metal, Dielectric

# Typing
num = int | float


def _clamp(x: num, mini: num, maxi: num) -> num:
    """
    Clamps the given number x inside the range (mini, maxi)
    :param x:
    :param mini:
    :param maxi:
    :return:
    """
    if x < mini:
        return mini
    if x > maxi:
        return maxi
    return x


def _lerp(a: num, b: num, t: num) -> num:
    """
    :param a:
    :param b:
    :param t:
    :return:
    """
    return (1 - t) * a + t * b


def _ray_color(ray: Ray, world: HittableList, depth: int) -> vec3.Vec3:
    """
    :param ray:
    :param world:
    :param depth
    :return:
    """
    if depth <= 0:
        return vec3.Vec3(0, 0, 0)
    hit = world.hit(ray, 0.001, math.inf)
    if hit is not None:
        interaction = hit.interact(ray)
        if interaction is not None:
            scattered, attenuation = interaction
            return attenuation * _ray_color(scattered, world, depth - 1)
    unit_dir = vec3.unit_vector(ray.direction)
    t = 0.5 * (unit_dir.y + 1)
    rp = _lerp(1, 0.5, t)
    gp = _lerp(1, 0.7, t)
    bp = _lerp(1, 1, t)
    return vec3.Vec3(rp, gp, bp)


def _sample_pix(cam: Camera, world: HittableList, i: int, j: int, img_w: int,
                img_h: int, samples: int, max_depth: int) -> vec3.Vec3:
    """
    :param cam:
    :param world:
    :param i:
    :param j:
    :param img_w:
    :param img_h:
    :param samples:
    :param max_depth:
    :return:
    """
    color = vec3.Vec3(0, 0, 0)
    for _ in range(samples):
        u = (i + random.random()) / (img_w - 1)
        v = (j + random.random()) / (img_h - 1)
        ray = cam.get_ray(u, v)
        color += _ray_color(ray, world, max_depth)
    return color


def _check_near_zero(n: num, eps: num = 1e-8) -> num:
    """
    :param n:
    :param eps:
    :return:
    """
    if abs(n) < eps:
        return n + eps
    return n


def render(fname: str, img_w: int, img_h: int, cam: Camera,
           world: HittableList, samples: int, max_depth: int) -> None:
    """
    Renders the image and writes it to a .ppm file
    :param fname: Name of the .ppm file
    :param img_w: Width of the image
    :param img_h: Height of the image
    :param cam: A Camera object
    :param world: List of the hittable objects
    :param samples: Samples per pixel
    :param max_depth:
    :return:
    """
    scale = 1 / samples
    with open(fname, "w") as f:
        f.write(f"P3\n{img_w} {img_h}\n255\n")
        for j in range(img_h - 1, -1, -1):
            print(f"Lines remaining: {j}", end=" ")
            s = default_timer()
            for i in range(img_w):
                color = _sample_pix(cam, world, i, j, img_w, img_h, samples,
                                    max_depth)
                r, g, b = color.x, color.y, color.z
                r = math.sqrt(scale * abs(r))
                g = math.sqrt(scale * abs(g))
                b = math.sqrt(scale * abs(b))
                ir = int(256 * _clamp(r, 0, 0.999))
                ig = int(256 * _clamp(g, 0, 0.999))
                ib = int(256 * _clamp(b, 0, 0.999))
                f.write(f"{ir} {ig} {ib}\n")
            e = default_timer()
            print(f"Estimated time: : {(e - s) * j / 60:.3f} min")


def random_scene() -> HittableList:
    """
    Returns a random scene with different kinds of spheres
    :return:
    """
    world = HittableList()
    mat_ground = Lambertian(vec3.Vec3(0.5, 0.5, 0.5))
    world.add(Sphere(vec3.Vec3(0, -1000, 0), 1000, mat_ground))
    for a in range(-5, 5):
        for b in range(-5, 5):
            choose_mat = random.random()
            x = a + 0.9 * random.random()
            y = 0.2
            z = b + 0.9 * random.random()
            center = vec3.Vec3(x, y, z)
            if (center - vec3.Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = vec3.rand_vect() * vec3.rand_vect()
                    material = Lambertian(albedo)
                    world.add(Sphere(center, y, material))
                elif choose_mat < 0.95:
                    albedo = vec3.rand_range_vect(0.5, 1)
                    fuzz = vec3.rand_range(0, 0.5)
                    material = Metal(albedo, fuzz)
                    world.add(Sphere(center, y, material))
                else:
                    material = Dielectric(1.5)
                    world.add(Sphere(center, y, material))

    material1 = Dielectric(1.5)
    world.add(Sphere(vec3.Vec3(0, 1, 0), 1, material1))
    material2 = Lambertian(vec3.Vec3(0.4, 0.2, 0.1))
    world.add(Sphere(vec3.Vec3(-4, 1, 0), 1, material2))
    material3 = Metal(vec3.Vec3(0.7, 0.6, 0.5), 0)
    world.add(Sphere(vec3.Vec3(4, 1, 0), 1, material3))
    return world


def main():
    fname = "images/final_scene_small.ppm"

    # Image
    aspect = 16 / 9
    img_w = 600
    img_h = int(img_w / aspect)

    # Camera
    lookfrom = vec3.Vec3(13, 2, 3)
    lookat = vec3.Vec3(0, 0, 0)
    vup = vec3.Vec3(0, 1, 0)
    vfov = 20
    aperture = 0.1
    focus_dist = 10
    cam = Camera(lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist)

    # Random world
    world = random_scene()

    # Render
    samples_per_pixel = 50
    max_depth = 10
    render(fname, img_w, img_h, cam, world, samples_per_pixel, max_depth)


if __name__ == "__main__":
    main()
