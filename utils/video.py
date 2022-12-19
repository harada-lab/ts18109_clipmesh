"""
    Helper class to create and add images to video
"""
import imageio
import numpy as np


class Video():
    def __init__(self, path, name='video_log.mp4', mode='I', fps=10, codec='libx264', bitrate='16M') -> None:
        
        if path[-1] != "/":
            path += "/"
        
        self.path = path
        self.name = name
        self.mode = mode
        self.fps = fps
        self.codec = codec
        self.bitrate = bitrate
        self.images = []

    def ready_image(self, image, write_video=True):
        # assuming channels last - as renderer returns it
        if len(image.shape) == 4: 
            image = image.squeeze(0)[..., :3].detach().cpu().numpy()
        else:
            image = image[..., :3].detach().cpu().numpy()

        image = np.clip(np.rint(image*255.0), 0, 255).astype(np.uint8)

        self.images.append(image)

        if write_video:
            print("writing video", self.path + self.name)
            writer = imageio.get_writer(self.path+self.name, mode=self.mode, fps=self.fps, codec=self.codec, bitrate=self.bitrate)
            for frame in self.images:
                writer.append_data(frame)
            writer.close()

        return image

    def close(self):
        #self.writer.close()
        return
