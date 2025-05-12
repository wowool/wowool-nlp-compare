from time import time
from functools import wraps
from memory_profiler import profile


@profile
def run_with_profiler(f, *args, **kw):
    return f(*args, **kw)


def profile_it(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = run_with_profiler(f, *args, **kw)
        te = time()
        print(f"Processing Time:{te-ts:.3f} sec", flush=True)
        return result

    return wrap
