"""
Raytracing in 2d

Class for a photon, i.e. the particle/ray whose path is traced
"""

import misc
import numpy as np
import matplotlib.pyplot as plt


class Photon:
    """
    A particle whose path will be traced
    """

    def __init__(self, pos: np.ndarray, direc: np.ndarray, ior: int | float = 1) -> None:
        """
        :param pos: Position vector
        :param direc: Direction vector
        :param ior: Current index of refraction
        """
        self.pos = pos
        self.direc = misc.norm(direc)
        self.ior = ior

    def plot_photon(self, length: int | float = 2, **kwargs) -> None:
        """
        Plots the photon as an arrow
        :param length: Length of the arrow
        :param kwargs: Keyword arguments accepted by quiver
        :return:
        """
        end = self.direc * length
        plt.arrow(float(self.pos[0]), float(self.pos[1]), float(end[0]),
                  float(end[1]), **kwargs)

    def translate(self, pos: np.ndarray) -> None:
        """
        Moves the photon to a new location
        :param pos: The new position as a vector
        :return:
        """
        self.pos = np.array(pos)
