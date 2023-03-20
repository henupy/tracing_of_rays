"""
Raytracing in 2d

Class for a photon, i.e. the particle/ray whose path is traced
"""

import misc
import numpy as np
import matplotlib.pyplot as plt

# Shortcuts for typing
numeric = int | float
vec = list | np.ndarray


class Photon:
    """
    A particle whose path will be traced
    """

    def __init__(self, pos: vec, direc: vec, ior: numeric = 1) -> None:
        """
        :param pos: Position vector
        :param direc: Direction vector
        :param ior: Current index of refraction
        """
        self.pos = np.array(pos)
        self.direc = misc.norm(direc)
        self.ior = ior

    def plot_photon(self, length: numeric = 2, **kwargs) -> None:
        """
        Plots the photon as an arrow
        :param length: Length of the arrow
        :param kwargs: Keyword arguments accepted by quiver
        :return:
        """
        end = self.direc * length
        plt.arrow(self.pos[0], self.pos[1], end[0], end[1], **kwargs)

    def translate(self, pos: vec) -> None:
        """
        Moves the photon to a new location
        :param pos: The new position as a vector
        :return:
        """
        self.pos = np.array(pos)
