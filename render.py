import numpy as np
import cv2
import math

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 10
TOTAL_FRAMES = FPS * DURATION

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("abstract_hd.mp4", fourcc, FPS, (WIDTH, HEIGHT))

for frame in range(TOTAL_FRAMES):
    phase = 2 * math.pi * frame / TOTAL_FRAMES
    
    y = np.linspace(0, 1, HEIGHT).reshape(-1, 1)
    wave = (np.sin(4 * np.pi * y + phase) + 1) / 2
    
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:, :, 0] = (wave * 255).astype(np.uint8)
    img[:, :, 1] = (wave * 150).astype(np.uint8)
    img[:, :, 2] = (wave * 80).astype(np.uint8)
    
    out.write(img)

out.release()
print("Selesai! Video berhasil dibuat.")