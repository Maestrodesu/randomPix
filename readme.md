[![Disclaimer](src/disclaimer.png)](Disclaimer)
# randomPix

randomPix is a Python + Ray + Pygame demo that generates and displays an endless stream of random RGB frames in real time.

## Features

- **Ray-based frame generator** with circular buffer
- **Batch frame production** to minimize overhead
- **Double-buffered rendering** to avoid freezes and stutters
- **Configurable resolution, buffer size, and batch size**
- **Non-blocking playback loop**: replays old frames while new ones are being prepared

## Requirements

- Python 3.9+
- [Ray](https://www.ray.io)
- [NumPy](https://numpy.org)
- [Pygame](https://www.pygame.org)

## Usage

```bash
python main.py
```
