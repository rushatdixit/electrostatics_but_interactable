"""Module for numerical solvers of Poisson's equation."""

import numpy as np
from constants import ITERATIONS

def get_potential(V: np.ndarray, rho: np.ndarray, iterations: int = ITERATIONS) -> np.ndarray:
    """
    Solves Poisson's equation numerically using the Jacobi iteration method.

    :param V: The current electrical potential grid.
    :type V: np.ndarray
    :param rho: The charge density grid.
    :type rho: np.ndarray
    :param iterations: Number of Jacobi sweeps to perform.
    :type iterations: int
    :return: The updated electrical potential grid after the specified iterations.
    :rtype: np.ndarray
    """
    for _ in range(iterations):
        V_old = V.copy()
        V[1:-1, 1:-1] = 0.25 * (
            V_old[2:, 1:-1] + V_old[:-2, 1:-1] +
            V_old[1:-1, 2:] + V_old[1:-1, :-2] +
            rho[1:-1, 1:-1]
        )
    return V