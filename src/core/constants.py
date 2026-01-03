import numpy as np
import os

window_width = 1920
window_height = 1080
rocket_accel_coeff = 1000.0
rocket_velocity_coeff = 1.0
rocket_start_position = np.array([window_height/2, window_width/2.0])
target_position = np.array([window_height, 0.0])
asteroid_radius = 20.0
asteroid_accel_coeff = 150.0
asteroid_vel_coeff = 1.0
asteroid_start_vel = 0
bullet_velocity = 1000

def generalise_height(height: int):
    return window_height*height//720
def generalise_width(width: int):
    return window_width*width//1280

def get_asset_path(*path_parts):
    """Get path to an asset file relative to project root."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(project_root, 'assets', *path_parts)

