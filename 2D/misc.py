"""
Miscellaneous functions used in multiple places
"""

import numpy as np

# For typing
numeric = int | float
vec = list | np.ndarray

def vector_len(v: vec) -> numeric:
    """
    Computes the length of the vector
    :param v:
    :return:
    """
    return np.sqrt(np.dot(v, v))


def norm(v: vec) -> vec:
    """
    Normalizes the vector
    :param v:
    :return:
    """
    return v / vector_len(v)


def rand_range(a: numeric, b: numeric) -> numeric:
    """
    Returns a random number on the semi-closed interval [a, b)
    :param a:
    :param b:
    :return:
    """
    return a + np.random.random() * (b - a)
