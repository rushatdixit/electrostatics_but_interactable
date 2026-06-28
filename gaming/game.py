"""Module defining the real-time Pygame simulator for electrostatics."""

import pygame 
# pyrefly: ignore [missing-import]
import numpy as np
from constants import (
    WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, ITERATIONS,
    CHARGE_MAGNITUDE, MAX_POTENTIAL_DISPLAY, MAX_EFIELD_DISPLAY,
    FPS, COLOR_POS_CHARGE, COLOR_NEG_CHARGE
)
from solving.potential_finder import get_potential
from solving.electric_field_finder import get_elec_field

class ElectroStaticsSimulator:
    """
    Manages the Pygame window and runs the real-time electrostatics simulation.
    """
    def __init__(self, RHO: np.ndarray) -> None:
        """
        Initializes the simulator with a starting charge distribution.

        :param RHO: The initial charge density grid.
        :type RHO: np.ndarray
        :return: None
        :rtype: None
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Charge Density Function : ")
        self.clock = pygame.time.Clock()
        self.running = True
        self.V = np.zeros((GRID_SIZE, GRID_SIZE))
        self.rho = RHO
        self.solving = False
        self.view_mode = 'potential'
        self.show_vectors = False
    
    def update(self) -> None:
        """
        Steps the simulation forward by solving Poisson's equation if solving is enabled.

        :return: None
        :rtype: None
        """
        if self.solving:
            self.V = get_potential(self.V, self.rho, ITERATIONS)
    
    def handle_events(self) -> None:
        """
        Handles all keyboard and mouse inputs during the game loop.

        :return: None
        :rtype: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
                
        buttons = pygame.mouse.get_pressed()
        if buttons[0] or buttons[2]:
            self.paint_charge(buttons)
    
    def handle_keydown(self, key: int) -> None:
        """
        Toggles application states based on keyboard presses.

        :param key: The integer ID of the key pressed.
        :type key: int
        :return: None
        :rtype: None
        """
        if key == pygame.K_SPACE:
            self.solving = not self.solving
        elif key == pygame.K_c:
            self.V.fill(0)
            self.rho.fill(0)
            self.solving = False
        elif key == pygame.K_v:
            self.view_mode = 'efield' if self.view_mode == 'potential' else 'potential'
        elif key == pygame.K_f:
            self.show_vectors = not self.show_vectors
        
    def paint_charge(self, buttons: tuple) -> None:
        """
        Maps mouse position to the simulation grid and paints charge onto it.

        :param buttons: Tuple of boolean states for the mouse buttons.
        :type buttons: tuple
        :return: None
        :rtype: None
        """
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // CELL_SIZE, my // CELL_SIZE
        
        if 0 < gx < GRID_SIZE - 1 and 0 < gy < GRID_SIZE - 1:
            if buttons[0]:
                self.rho[gy, gx] = CHARGE_MAGNITUDE
            if buttons[2]:
                self.rho[gy, gx] = -CHARGE_MAGNITUDE
        
    def draw(self) -> None:
        """
        Renders the potential field or electric field magnitude to the Pygame screen.

        :return: None
        :rtype: None
        """
        EF = get_elec_field(self.V)
        Ex = EF.x_component
        Ey = EF.y_component
        E_mag = EF.magnitude

        color_array = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=np.uint8)

        if self.view_mode == 'potential':
            V_clamp = np.clip(self.V.T, -MAX_POTENTIAL_DISPLAY, MAX_POTENTIAL_DISPLAY)
            color_array[..., 0] = np.where(V_clamp > 0, V_clamp * (255.0 / MAX_POTENTIAL_DISPLAY), 0)
            color_array[..., 2] = np.where(V_clamp < 0, -V_clamp * (255.0 / MAX_POTENTIAL_DISPLAY), 0)
            
        elif self.view_mode == 'efield':
            E_clamp = np.clip(E_mag.T, 0, MAX_EFIELD_DISPLAY) 
            color_array[..., 1] = (E_clamp / MAX_EFIELD_DISPLAY * 255.0).astype(np.uint8)
        
        color_array[self.rho.T > 0] = COLOR_POS_CHARGE
        color_array[self.rho.T < 0] = COLOR_NEG_CHARGE

        surf = pygame.surfarray.make_surface(color_array)
        scaled_surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
        self.screen.blit(scaled_surf, (0, 0))

        if self.show_vectors:
            self.draw_vectors(Ex, Ey, E_mag)
    
    def draw_vectors(self, Ex: np.ndarray, Ey: np.ndarray, E_mag: np.ndarray) -> None:
        """
        Draws electric field vectors over the screen to visualize directionality.

        :param Ex: The x-components of the electric field.
        :type Ex: np.ndarray
        :param Ey: The y-components of the electric field.
        :type Ey: np.ndarray
        :param E_mag: The magnitude of the electric field.
        :type E_mag: np.ndarray
        :return: None
        :rtype: None
        """
        step = 5
        vector_color = (255, 255, 255) if self.view_mode == 'potential' else (200, 200, 255)
        
        for gy in range(step, GRID_SIZE - step, step):
            for gx in range(step, GRID_SIZE - step, step):
                mag = E_mag[gy, gx]
                if mag > 0.1:
                    ex_norm = Ex[gy, gx] / mag
                    ey_norm = Ey[gy, gx] / mag
                    
                    sx = gx * CELL_SIZE + CELL_SIZE // 2
                    sy = gy * CELL_SIZE + CELL_SIZE // 2
                    end_x = sx + (ex_norm * CELL_SIZE * 2.5)
                    end_y = sy + (ey_norm * CELL_SIZE * 2.5)
                    
                    pygame.draw.line(self.screen, vector_color, (sx, sy), (end_x, end_y), 1)
                    pygame.draw.circle(self.screen, vector_color, (int(end_x), int(end_y)), 2)
    
    def run(self) -> None:
        """
        The main blocking loop of the game. Handles frames and rendering.

        :return: None
        :rtype: None
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()