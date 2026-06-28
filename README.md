# Electrostatics Simulator

A robust 2D electrostatics solver and visualizer written in Python. This project computes the electrical potential and electric field lines for any user-defined charge density distribution using numerical methods. 

It features two distinct modes:
1. **Interactable Mode (Pygame)**: A real-time sandbox where the user can paint charges onto a grid and observe the electrical potential naturally diffuse and reach equilibrium at 60 FPS.
2. **Analytic Mode (Matplotlib)**: A mathematically rigorous solver that computes the potential field up to a strict convergence limit, outputting a high-quality topological heatmap and streamline plot of the electric field.

---

## Sample Results

### Analytic Solver Output (Dipole)
![Analytic Solver Dipole](sample_results/analytic_dipole.png)

### Real-Time Pygame Output (Dipole)
*Potential Heatmap (Left) and E-Field Magnitude (Right)*

<p align="center">
  <img src="sample_results/pygame_potential.png" width="45%" />
  <img src="sample_results/pygame_efield.png" width="45%" />
</p>

---

## The Mathematics

### 1. Poisson's Equation
In electrostatics, the electrical potential $V$ at any point in space is directly related to the charge density $\rho$ at that point by Poisson's Equation:
$$ \nabla^2 V = -\frac{\rho}{\epsilon_0} $$
This simulator normalizes the constants (treating $\epsilon_0 = 1$) to solve: 
$$ \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} = -\rho $$

### 2. The Jacobi Method (Numerical Solver)
To solve this differential equation on a 2D discrete grid, the finite difference method is utilized. Approximating the second derivatives using the values of neighboring grid cells and rearranging the equation yields the Jacobi Iteration formula:
$$ V_{i,j} = \frac{1}{4}(V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1} + \rho_{i,j}) $$

This algorithm functions as a relaxation method. By calculating the average of the four surrounding cells and adding the localized charge iteratively, the mathematical errors gradually diffuse until the numerical grid converges to the true potential field.

### 3. The Electric Field
The Electric Field $\mathbf{E}$ is the negative gradient of the potential $V$:
$$ \mathbf{E} = -\nabla V $$
Once the potential field $V$ is solved, the simulator calculates the numerical derivative in both the X and Y directions to define the continuous vector field of the electric field.

---

## Sample Density Functions
You can modify `density_function(x, y)` in `main.py` to simulate various physical scenarios. The following represent standard theoretical density functions encountered in electrostatics:

### 1. Point Charge
A single localized point of charge.
```python
def point_charge(x: int, y: int) -> float:
    return 1000.0 if (x == 50 and y == 50) else 0.0
```

### 2. Electric Dipole
Two equal but opposite charges separated by a defined distance.
```python
def electric_dipole(x: int, y: int) -> float:
    if x == 40 and y == 50:
        return -100.0
    elif x == 60 and y == 50:
        return 100.0
    return 0.0
```

### 3. Infinite Line Charge
A continuous straight line of uniform charge density.
```python
def line_charge(x: int, y: int) -> float:
    return 100.0 if x == 50 else 0.0
```

### 4. Parallel Plate Capacitor
Two parallel plates bearing opposite charges, generating a uniform internal electric field.
```python
def parallel_plates(x: int, y: int) -> float:
    if x == 30 and 20 <= y <= 80:
        return -100.0
    elif x == 70 and 20 <= y <= 80:
        return 100.0
    return 0.0
```
