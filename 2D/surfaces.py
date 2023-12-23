"""
Raytracing in 2d

Classes for different types of surfaces
"""

import misc
import numpy as np
import matplotlib.pyplot as plt

from photon import Photon


class Surface:
    """
    Represents a straight non-reflective surface, supposed to be used as
    a boundary that lets the photons through, i.e. a non-reflective
    boundary condition
    """
    def __init__(self, pos: np.ndarray, direc: np.ndarray, length: int | float) -> None:
        """
        :param pos: Position of the mirror's corner
        :param direc: Direction of the mirror's normal vector
        :param length: Length of the mirror (only used for plotting)
        """
        self.pos = pos
        self.norm = misc.norm(v=direc)
        self.adj = np.array([self.norm[1], -self.norm[0]])
        self.length = length
        self.alpha = 0.2

    def plot_wall(self, **kwargs):
        """
        Plots the wall
        :param kwargs: Keyword arguments for a lineplot
        :return:
        """
        end = self.adj * self.length + self.pos
        plt.plot([self.pos[0], end[0]], [self.pos[1], end[1]],
                 alpha=self.alpha, **kwargs)

    @staticmethod
    def interact(p: Photon, pos: np.ndarray) -> None:
        """
        Interacts with the photon, i.e. places it along the boundary
        :param p: A photon object
        :param pos: The location of the interaction
        :return:
        """
        p.translate(pos=pos)


class Mirror(Surface):
    """
    Represents a straight reflective wall, i.e. a mirror, in the geometry
    """

    def __init__(self, pos: np.ndarray, direc: np.ndarray, length: int | float) -> None:
        """
        :param pos: Position of the mirror's corner
        :param direc: Direction of the mirror's normal vector
        :param length: Length of the mirror (only used for plotting)
        """
        super().__init__(pos, direc, length)
        self.alpha = 1

    def interact(self, p: Photon, pos: np.ndarray) -> None:
        """
        Reflects the photon of the surface
        :param p: A Photon object
        :param pos: Location of the interaction
        :return:
        """
        p.direc = p.direc - 2 * np.dot(p.direc, self.norm) * self.norm
        p.translate(pos=pos)
