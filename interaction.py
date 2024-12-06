"""
Raytracing in 2d

Class for a interaction between the photon and a surface
"""

import numpy as np

from surfaces import Mirror

# Shortcut for typing
surface = Mirror


class Interaction:
    """
    Indicates a hit
    """
    def __init__(self, surf: surface, time: int | float,
                 point: np.ndarray) -> None:
        """
        :param surf: A surface object that has intersected with a photon
        :param time: The time it takes for the photon to reach the
        intersection point
        :param point: The location of the intersection
        """
        self.surf = surf
        self.time = time
        self.point = point

    def __repr__(self) -> str:
        """
        Nice representation of a collision
        :return:
        """
        return f"Collision at {self.point[0], self.point[1]}"
