import pygame
from frame_gen import RGBGenerator
import ray


def run_game(width, height, frames):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("randomPix")

    clock = pygame.time.Clock()
    running = True
    frame_idx = 0

    while running and frame_idx < len(frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # отрисовка текущего кадра
        surface = pygame.surfarray.make_surface(frames[frame_idx])
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        frame_idx = (frame_idx + 1) % len(frames)
        clock.tick(120)  # ограничение FPS

    pygame.quit()


def unlim_run(width=1000, height=1000, batch_size=100, fps=30):
    ray.init()
    generator = RGBGenerator.remote(buffer_size=100, width=width, height=height)

    # Инициализируем начальный фронтовой буфер
    ray.get(generator.add_frames.remote(batch_size=batch_size))
    front_buffer = ray.get(generator.get_latest_frames.remote(batch_size))
    back_buffer_ref = None
    pending_ref = None
    frame_idx = 0

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("randomPix")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(front_buffer) > 0:
            surface = pygame.surfarray.make_surface(front_buffer[frame_idx])
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            frame_idx = (frame_idx + 1) % len(front_buffer)

        # Если не запущено обновление — запускаем
        if pending_ref is None:
            pending_ref = generator.add_frames.remote(batch_size=batch_size)
            back_buffer_ref = generator.get_latest_frames.remote(batch_size)

        # Проверяем, готов ли новый батч (не блокируемся!)
        ready, _ = ray.wait([back_buffer_ref], timeout=0)
        if ready:
            try:
                # подхватываем новый буфер
                front_buffer = ray.get(back_buffer_ref)
                frame_idx = 0
            finally:
                pending_ref = None
                back_buffer_ref = None

        clock.tick(fps)

    pygame.quit()
    ray.shutdown()
