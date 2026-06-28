"""Module defining physical objects and data structures used in the simulation."""

import numpy as np

class Field:
    """
    Represents a vector field with X and Y components alongside its magnitude.
    """
    def __init__(self, x_component: np.ndarray, y_component: np.ndarray, magnitude: np.ndarray):
        """
        Initializes the Field object.

        :param x_component: The x-components of the vectors across the grid.
        :type x_component: np.ndarray
        :param y_component: The y-components of the vectors across the grid.
        :type y_component: np.ndarray
        :param magnitude: The magnitude of the vectors across the grid.
        :type magnitude: np.ndarray
        """
        self.x_component = x_component
        self.y_component = y_component
        self.magnitude = magnitude