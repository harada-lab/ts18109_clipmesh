# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

import argparse
import os
from time import sleep
from typing import List

import pymeshlab
import torch
from cog import BasePredictor, Input, Path

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Predictor(BasePredictor):
    def setup(self):
        os.system("bash /initialize.sh")
        return

    def predict(
        self,
        text_prompt: str = Input(description="Text to render", default="A blue robotic cat. Unreal engine. Trending on artstation."),
        seed: int = Input(description="random seed", default=123),
        epoch: int = Input(description="training epochs", default=1000),
        lr: float = Input(description="maximum learning rate", default=0.01),
        train_res: int = Input(description="Resolution of render before scaling to 224x224. must be a multiple of 8", default=384),
        texture_resolution: int = Input(description="resolution of texture maps", default=512),
        batch_size: int = Input(description="How many images of shape are rendered at one epoch)", default=50),
        scales: float = Input(description="Scale mesh size by some value", default=2.0)
    ) -> Path:
         
        print("output path before running: ")
        os.system("ls -l /outputs/")
        os.system(f"""
            python main.py \\
                --config configs/single.yml \\
                --text_prompt "{text_prompt}" \\
                --seed {seed} \\
                --epoch {epoch} \\
                --lr {lr} \\
                --train_res {train_res} \\
                --scales {scales} \\
                --batch_size {batch_size} \\
                --texture_resolution {texture_resolution} \\
        """)
        print("output path after running: ")
        os.system("ls -l /outputs/")

        # ms = pymeshlab.MeshSet()

        # ms.load_new_mesh(target_path)
        
        # # run filter meshing_invert_face_orientation
        # ms.meshing_invert_face_orientation()
        # ms.compute_color_transfer_vertex_to_face()
        # ms.meshing_decimation_quadric_edge_collapse(targetfacenum=6500)
        # ms.save_current_mesh(target_path) 

        # text_slug = slugify(text)




        # save as glb file
        target_glb_path = os.path.join("/outputs",f"z_output.glb")
        print("running ", f"obj2gltf -i /outputs/meshes/mesh_0/mesh.obj -o {target_glb_path}")
        
        os.system(f"obj2gltf -i  /outputs/meshes/mesh_0/mesh.obj -o {target_glb_path}")

        # return Path(target_path)
        return Path("/outputs/meshes/mesh_0/mesh.obj")

