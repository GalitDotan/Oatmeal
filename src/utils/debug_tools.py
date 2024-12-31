import os
import time
from collections import defaultdict

OUT_DIR = 'out'


def write_to_dot(transducer, file_name):
    os.makedirs(OUT_DIR, exist_ok=True)  # make sure the directory exists
    path = os.path.join(OUT_DIR, file_name + ".dot")
    with open(path, "w") as file:
        file.write(transducer.dot_representation())


run_times_by_function_names = defaultdict(list)


def timeit(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        delta = end_time - start_time
        run_times_by_function_names[method.__name__].append(delta)

        return result

    return timed
