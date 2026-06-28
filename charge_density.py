"""Module for managing and assigning charge density distributions over the simulation grid."""

from constants import GRID_SIZE
import numpy as np
from typing import Callable

rho = np.zeros((GRID_SIZE, GRID_SIZE))

def set_rho(density_function: Callable[[int, int], float], rho: np.ndarray, x_min: int, y_min: int, x_max: int, y_max: int) -> np.ndarray:
    """
    Populates the charge density grid by applying a density function over a bounding region.

    :param density_function: A function that takes x and y coordinates and returns a charge value.
    :type density_function: Callable[[int, int], float]
    :param rho: The 2D numpy array representing the charge density grid.
    :type rho: np.ndarray
    :param x_min: The minimum x-coordinate of the bounding box.
    :type x_min: int
    :param y_min: The minimum y-coordinate of the bounding box.
    :type y_min: int
    :param x_max: The maximum x-coordinate of the bounding box.
    :type x_max: int
    :param y_max: The maximum y-coordinate of the bounding box.
    :type y_max: int
    :return: The updated charge density grid.
    :rtype: np.ndarray
    """
    x_start, x_end = min(x_min, x_max), max(x_min, x_max)
    y_start, y_end = min(y_min, y_max), max(y_min, y_max)
    for i in range(x_start, x_end + 1):
        for j in range(y_start, y_end + 1):
            rho[j, i] = density_function(i, j)
    return rho