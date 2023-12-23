"""
Miscellaneous functions used in multiple places
"""

import numpy as np


def vector_len(v: np.ndarray) -> int | float:
    """
    Computes the length of the vector
    :param v:
    :return:
    """
    return np.sqrt(np.dot(v, v))


def norm(v: np.ndarray) -> np.ndarray:
    """
    Normalizes the vector
    :param v:
    :return:
    """
    return v / vector_len(v)


def rand_range(a: int | float, b: int | float) -> int | float:
    """
    Returns a random number on the semi-closed interval [a, b)
    :param a:
    :param b:
    :return:
    """
    return a + np.random.random() * (b - a)
