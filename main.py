import multiprocessing
from engine import unlim_run

width, height = 800, 800

if __name__ == "__main__":
    p = multiprocessing.Process(target=unlim_run(width, height))
    p.start()
    p.join()
