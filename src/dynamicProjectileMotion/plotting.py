import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from dynamicProjectileMotion.projectile import Projectile

def interactive_plot():
    initial_velocity = 20.0
    launch_angle = 45.0
    dt = 0.01
    t_max = 10.0
    drag = False

    # create the figure and axis
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.3)

    # run the simulation
    projectile = Projectile(initial_velocity, launch_angle, dt, t_max, drag=drag)
    t,x,y = projectile.simulation()

    # plot the trajectory
    trajectory, = ax.plot(x, y, lw=2, label='Trajectory')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Height (m)')
    ax.set_title('Projectile Motion')
    ax.grid(True)
    ax.legend()

    # set appropriate limits
    ax.set_xlim(0, np.max(x))
    ax.set_ylim(0, np.max(y))

    # create the sliders
    ax_angle = plt.axes([0.1, 0.15, 0.8, 0.03])
    angle_slider = widgets.Slider(ax_angle, 'Launch Angle', 0, 90, valinit=launch_angle)

    ax_velocity = plt.axes([0.1, 0.1, 0.8, 0.03])
    velocity_slider = widgets.Slider(ax_velocity, 'Initial Velocity', 0, 100, valinit=initial_velocity)

    # create a button to consider air drag
    ax_drag = plt.axes([0.1, 0.05, 0.1, 0.04])
    drag_button = widgets.Button(ax_drag, 'Air Drag', color='lightgoldenrodyellow')

    current_drag = [drag]

    def update(val):
        angle = angle_slider.val
        velocity = velocity_slider.val
        drag = current_drag[0]

        projectile = Projectile(velocity, angle, dt, t_max, drag=drag)
        t,x,y = projectile.simulation()

        trajectory.set_xdata(x)
        trajectory.set_ydata(y)

        ax.set_xlim(0, np.max(x))
        ax.set_ylim(0, np.max(y))
        fig.canvas.draw_idle()

    def toggle_drag(event):
        current_drag[0] = not current_drag[0]
        update(None)
    
    angle_slider.on_changed(update)
    velocity_slider.on_changed(update)
    drag_button.on_clicked(toggle_drag)

    plt.show()