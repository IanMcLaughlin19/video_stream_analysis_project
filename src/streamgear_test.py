from vidgear.gears import StreamGear
import cv2
import qrcode
import time
import random
import threading
import os
from PIL import Image
from typing import Dict, Tuple

DEFAULT_FRAMERATE = float(os.environ.get("FPS", 25.0))
DEFAULT_IMAGE_SIZE = 1

IMAGE_SIZE_MAP: Dict[int, Tuple[int, int]] = {
    0: (486, 240),
    1: (720, 480),
    2: (1280, 720),
    3: (1440, 1080)
}

IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", DEFAULT_IMAGE_SIZE))
print(f"Image siz: {IMAGE_SIZE}")
IMAGE_DIMENSIONS = IMAGE_SIZE_MAP[IMAGE_SIZE]

# Provides a scaling of image sizes from 1 - 10
# FPS configuration would be important
# Could do prerecorded QR code video
# There's definitely CPU and memory

def start_stream(framerate: float=DEFAULT_FRAMERATE, output: str="video\\stream.m3u8", stream_frame_limit: int=None) -> None:
    """
    Starts streaming qr code video to network stream
    """
    options_stream = {"-livestream": True, "-input_framerate": framerate}
    streamer = StreamGear(output=output, format="hls", **options_stream)
    counter = 0
    while True:
        # Two params is probably the size of the frames width and ehight
        qr_code_data = {"frame_number": counter, "time": time.time(), "random": random.random()}
        qr_code = qrcode.make(data=qr_code_data)
        qr_code.save("temp.png")
        frame = cv2.imread("temp.png")
        if IMAGE_SIZE != DEFAULT_IMAGE_SIZE:
            width, height = IMAGE_DIMENSIONS[0], IMAGE_DIMENSIONS[1]
            frame = cv2.resize(frame, (width, height))
        streamer.stream(frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            print("Stream manually terminated. Ending now...")
            break
        if stream_frame_limit is not None and counter > stream_frame_limit:
            print(f"Ending stream because {counter} frames have been sent")
            break
        counter += 1
    streamer.terminate()


if __name__ == '__main__':
    start_stream()
