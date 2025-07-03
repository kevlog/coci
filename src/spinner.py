import sys
import time
import itertools

# Spinner
def spinner(text, stop_event):
    dots = itertools.cycle(['.', '..', '...'])
    space = itertools.cycle(['   '])
    frame = 0
    dot = next(dots)

    while not stop_event.is_set():
        if frame % 5 == 0:
            dot = next(dots)
        sys.stdout.write(f'\r[INFO] {text}{dot}{next(space)}')
        sys.stdout.flush()
        time.sleep(0.1)
        frame += 1