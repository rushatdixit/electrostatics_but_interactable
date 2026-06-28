"""Main entry point for the Electrostatics Simulator."""

from gaming.game import ElectroStaticsSimulator
from charge_density import set_rho, rho
import numpy as np

def density_function(x: int, y: int) -> float:
    """
    User-defined charge density function.

    :param x: The x-coordinate on the grid.
    :type x: int
    :param y: The y-coordinate on the grid.
    :type y: int
    :return: The charge density at the specified coordinates.
    :rtype: float
    """
    return -100 if x <= 50 else 100

if __name__ == "__main__":
    mode = input("Choose mode - Interactable (1) or Analytic (2): ").strip()
    
    print("Make sure you have entered your density function....")
    try:
        x_min = int(input("Enter x_min [default 45]: ") or "45")
        y_min = int(input("Enter y_min [default 45]: ") or "45")
        x_max = int(input("Enter x_max [default 55]: ") or "55")
        y_max = int(input("Enter y_max [default 55]: ") or "55")
    except ValueError:
        x_min, y_min, x_max, y_max = 45, 45, 55, 55
        
    RHO = set_rho(density_function, rho, x_min, y_min, x_max, y_max)
    
    if mode == "2":
        from solve_analytically import solve_and_plot
        solve_and_plot(RHO)
    else:
        app = ElectroStaticsSimulator(RHO)
        app.run()