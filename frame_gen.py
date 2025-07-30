import ray
import numpy as np
from numpy.random import Generator, PCG64


@ray.remote
class RGBGenerator:
    def __init__(self, buffer_size=100, width=256, height=256):
        self.buffer_size = buffer_size
        self.width = width
        self.height = height
        self.buffer = np.empty((buffer_size, height, width, 3), dtype=np.uint8)
        self.head = 0
        self.full = False
        self.rng = Generator(PCG64())

    def add_frames(self, batch_size=10):
        """Генерирует batch_size кадров и добавляет их в буфер"""
        new_frames = self.rng.integers(
            0, 256, (batch_size, self.height, self.width, 3), dtype=np.uint8
        )

        for frame in new_frames:
            self.buffer[self.head] = frame
            self.head = (self.head + 1) % self.buffer_size
            if self.head == 0:
                self.full = True
        return True

    def get_latest_frames(self, n):
        """Возвращает последние n кадров"""
        size = self.buffer_size if self.full else self.head
        n = min(n, size)
        start = (self.head - n) % self.buffer_size

        if start < self.head or (self.full and start > self.head):
            return self.buffer[start : self.head].copy()
        else:
            return np.concatenate(
                [self.buffer[start:], self.buffer[: self.head]]
            ).copy()
