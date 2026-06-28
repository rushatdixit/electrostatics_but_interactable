"""Module containing the analytical convergence solver and Matplotlib visualization."""

import numpy as np
import matplotlib.pyplot as plt
from constants import GRID_SIZE, EPSILON
from solving.potential_finder import get_potential
from solving.electric_field_finder import get_elec_field

def solve_and_plot(rho: np.ndarray) -> None:
    """
    Solves the potential field until mathematical convergence is reached and visualizes the results.

    :param rho: The initial charge density grid.
    :type rho: np.ndarray
    :return: None
    :rtype: None
    """
    print(f"Starting analytical solver. Convergence limit (EPSILON): {EPSILON}")
    
    V = np.zeros((GRID_SIZE, GRID_SIZE))
    
    iterations = 0
    while True:
        V_old = V.copy()
        V = get_potential(V, rho, iterations=1)
        iterations += 1
        
        max_diff = np.max(np.abs(V - V_old))
        if max_diff < EPSILON:
            break
            
    print(f"Converged after {iterations} iterations!")
    
    EF = get_elec_field(V)
    Ex = EF.x_component
    Ey = EF.y_component
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    heatmap = ax.imshow(V, cmap='RdBu', origin='lower', extent=[0, GRID_SIZE, 0, GRID_SIZE])
    plt.colorbar(heatmap, label="Electric Potential (V)")
    
    Y, X = np.mgrid[0:GRID_SIZE, 0:GRID_SIZE]
    
    ax.streamplot(X, Y, Ex, Ey, color='k', linewidth=1, density=1.5, arrowsize=1.2)
    
    ax.set_title(f"Potential Heatmap and E-Field Lines\n(Converged in {iterations} iterations)")
    ax.set_xlabel("X (Grid Units)")
    ax.set_ylabel("Y (Grid Units)")
    
    plt.show()

if __name__ == "__main__":
    # Fallback default hardcoded region for testing standalone
    from charge_density import set_rho
    print("Running solve_analytically.py standalone with hardcoded test region...")
    rho = np.zeros((GRID_SIZE, GRID_SIZE))
    
    def test_density(x: int, y: int) -> float:
        return 100.0 if x > 50 else -100.0
        
    rho = set_rho(test_density, rho, 40, 40, 60, 60)
    solve_and_plot(rho)
