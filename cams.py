import os
#import clip
import kornia
import matplotlib.pyplot as plt
import numpy as np
import nvdiffrast.torch as dr
import torch
import torchvision
import yaml
from dalle2_pytorch import DiffusionPrior, DiffusionPriorNetwork
from PIL import Image
from tqdm import tqdm
import glm

def persp_proj(fov_x=45, ar=1, near=1.0, far=50.0):
    """
    From https://github.com/rgl-epfl/large-steps-pytorch by @bathal1 (Baptiste Nicolet)

    Build a perspective projection matrix.
    Parameters
    ----------
    fov_x : float
        Horizontal field of view (in degrees).
    ar : float
        Aspect ratio (w/h).
    near : float
        Depth of the near plane relative to the camera.
    far : float
        Depth of the far plane relative to the camera.
    """
    fov_rad = np.deg2rad(fov_x)

    tanhalffov = np.tan( (fov_rad / 2) )
    max_y = tanhalffov * near
    min_y = -max_y
    max_x = max_y * ar
    min_x = -max_x

    z_sign = -1.0
    proj_mat = np.array([[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

    proj_mat[0, 0] = 2.0 * near / (max_x - min_x)
    proj_mat[1, 1] = 2.0 * near / (max_y - min_y)
    proj_mat[0, 2] = (max_x + min_x) / (max_x - min_x)
    proj_mat[1, 2] = (max_y + min_y) / (max_y - min_y)
    proj_mat[3, 2] = z_sign

    proj_mat[2, 2] = z_sign * far / (far - near)
    proj_mat[2, 3] = -(far * near) / (far - near)
    
    return proj_mat





log_elev = 30.0
log_dist = 8.0
rot_ang  = 0.0
look_at=[0, 0, 0]
up=[0, -1, 0]
for rot_ang in range(100):
    print(str(rot_ang) + "回目")
    elev_angle  = log_elev
    azim_angle  = float(rot_ang)
    distance    = log_dist

    elev = np.radians(elev_angle)
    azim = np.radians(azim_angle)

    cam_z = distance * np.cos(elev) * np.sin(azim)
    cam_y = distance * np.sin(elev)
    cam_x = distance * np.cos(elev) * np.cos(azim)
    modl = glm.mat4()
    view = glm.lookAt(
        glm.vec3(cam_x, cam_y, cam_z),
        glm.vec3(look_at[0], look_at[1], look_at[2]),
        glm.vec3(up[0], up[1], up[2]),
    )
    a_mv = view * modl
    a_mv = np.array(a_mv.to_list()).T
    proj_mtx = persp_proj(60)    
    a_mvp = np.matmul(proj_mtx, a_mv).astype(np.float32)[None, ...]    
    a_lightpos = np.linalg.inv(a_mv)[None, :3, 3]
    a_campos = a_lightpos

    print("cam_x is "+ str(cam_x) + "\n")
    print("cam_y is "+ str(cam_y) + "\n")
    print("cam_z is "+ str(cam_z) + "\n")

    print("view is \n")
    print(view)
    print("\n")

    print("a_mv is\n")
    print(a_mv)
    print("\n")

    print("a_campos is\n")
    print(a_campos)
    print("\n")

    type(a_campos)