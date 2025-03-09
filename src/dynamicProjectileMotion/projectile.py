import numpy as np
import scipy.constants as const

G = const.g # acceleration due to gravity
DRAG_COEFF = 0.47 # drag coefficient for a sphere
AIR_DENSITY = 1.225 # air density at sea level
CROSS_SECTION = 0.01 # cross-sectional area of a sphere


class Projectile:
    '''
        Initialize the projectile object with the following parameters:
            v0: float representing the initial velocity of the projectile
            theta: float representing the launch angle of the projectile
            dt: float representing the time step of the simulation
            t_max: float representing the maximum time of the simulation
            g: float representing the acceleration due to gravity
            drag: bool representing whether to include air drag in the simulation
            drag_coeff: float representing the drag coefficient of the projectile
            air_density: float representing the air density at sea level
            cross_section: float representing the cross-sectional area of the projectile
    '''

    def __init__(self, v0: float, theta: float, dt: float, t_max: float, g=G, 
                 drag: bool = False, drag_coeff: float = DRAG_COEFF, 
                 air_density: float = AIR_DENSITY, 
                 cross_section: float = CROSS_SECTION):
        
        if v0 < 0:
            raise ValueError("Initial velocity must be greater than zero")
        if theta < 0 or theta > 90:
            raise ValueError("Launch angle must be between 0 and 90 degrees")
        if dt <= 0:
            raise ValueError("Time step must be greater than zero")
        if t_max <= 0:
            raise ValueError("Maximum time must be greater than zero")

        self.v0 = v0
        self.theta = np.radians(theta)
        self.dt = dt
        self.t_max = t_max
        self.g = g
        self.drag = drag
        self.drag_coeff = drag_coeff
        self.air_density = air_density
        self.cross_section = cross_section
        self.t = None
        self.x = None
        self.y = None

    def simulation(self):
        # initialize the velocity components
        vx = self.v0 * np.cos(self.theta)
        vy = self.v0 * np.sin(self.theta) 

        # initialize the position and time arrays
        t_values = [0]
        x_values = [0]
        y_values = [0]

        t = 0.0
        x = 0.0
        y = 0.0

        # simulate the projectile motion
        while t < self.t_max and y >= 0:
            if self.drag:
                # calculate the inital velocity
                v = np.sqrt(vx**2 + vy**2)

                # calculate the drag force
                F_drag = 0.5 * self.drag_coeff * self.air_density * self.cross_section * v**2

                # calculate the drag acceleration (assuming mass = 1 for simplicity)
                ax_drag = -F_drag * (vx / v)
                ay_drag = -F_drag * (vy / v)
            else:
                ax_drag = 0
                ay_drag = 0

            # calculate the acceleration components
            ax = ax_drag
            ay = -self.g + ay_drag

            # update the velocity components
            vx += ax * self.dt
            vy += ay * self.dt

            # update the position components
            x += vx * self.dt
            y += vy * self.dt

            # update the time
            t += self.dt

            # append the values to the arrays
            t_values.append(t)
            x_values.append(x)
            y_values.append(y)

            # if the projectile hits the ground, break the loop
            if y < 0:
                break

            self.t = np.array(t_values)
            self.x = np.array(x_values)
            self.y = np.array(y_values)

        return self.t, self.x, self.y
    
    def get_max_height(self):
        if self.y is None:
            self.simulation()
        return np.max(self.y)

    def get_max_range(self):
        if self.x is None:
            self.simulation()
        return np.max(self.x)

    def get_time_of_flight(self):
        if self.t is None:
            self.simulation()
        return self.t[-1]