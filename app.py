from fastapi import FastAPI
from fastapi.responses import FileResponse
import numpy as np
import cv2
import math

app = FastAPI()

WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION = 8
TOTAL_FRAMES = FPS * DURATION

def generate_wave(frame):
    phase = 2 * math.pi * frame / TOTAL_FRAMES
    y = np.linspace(0, 1, HEIGHT).reshape(-1, 1)
    wave = (np.sin(6 * math.pi * y + phase) + 1) / 2
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:, :, 0] = (wave * 255).astype(np.uint8)
    img[:, :, 1] = (wave * 120).astype(np.uint8)
    img[:, :, 2] = (wave * 60).astype(np.uint8)
    return img

def generate_radial(frame):
    phase = 2 * math.pi * frame / TOTAL_FRAMES
    x = np.linspace(-1, 1, WIDTH)
    y = np.linspace(-1, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)
    r = np.sqrt(xv**2 + yv**2)
    wave = (np.sin(10 * r - phase) + 1) / 2
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:, :, 0] = (wave * 200).astype(np.uint8)
    img[:, :, 1] = (wave * 80).astype(np.uint8)
    img[:, :, 2] = (wave * 255).astype(np.uint8)
    return img

def generate_plasma(frame):
    phase = frame / TOTAL_FRAMES
    x = np.linspace(0, 4, WIDTH)
    y = np.linspace(0, 4, HEIGHT)
    xv, yv = np.meshgrid(x, y)
    wave = (np.sin(xv + phase*6) + np.sin(yv + phase*6)) / 2
    wave = (wave + 1) / 2
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:, :, 0] = (wave * 255).astype(np.uint8)
    img[:, :, 1] = (wave * 200).astype(np.uint8)
    img[:, :, 2] = (wave * 100).astype(np.uint8)
    return img

@app.get("/generate/{style}")
def generate_video(style: str):
    filename = f"{style}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))

    for frame in range(TOTAL_FRAMES):
        if style == "wave":
            img = generate_wave(frame)
        elif style == "radial":
            img = generate_radial(frame)
        elif style == "plasma":
            img = generate_plasma(frame)
        else:
            img = generate_wave(frame)

        out.write(img)

    out.release()
    return FileResponse(filename, media_type="video/mp4", filename=filename)