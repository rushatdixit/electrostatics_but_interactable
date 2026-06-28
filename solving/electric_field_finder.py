"""Module for calculating electric fields from electrical potential fields."""

import numpy as np
from objects import Field

def get_elec_field(V: np.ndarray) -> Field:
    """
    Calculates the electric field vectors and magnitude from a given potential field.

    :param V: The electrical potential grid.
    :type V: np.ndarray
    :return: A Field object containing the X and Y components and the overall magnitude.
    :rtype: Field
    """
    Ey, Ex = np.gradient(V)
    Ex = -Ex
    Ey = -Ey
    E_mag = np.sqrt(Ex**2 + Ey**2)
    return Field(Ex, Ey, E_mag)