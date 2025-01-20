import time
import os
import psutil
from functools import wraps


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def get_current_memory_usage():
    vm = psutil.virtual_memory()
    print(vm)
    return vm.used


def nlp_profile(name: str | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if name:
                func_name = name
            else:
                func_name = func.__name__
            mem_before = get_process_memory()
            sys_mem_before = get_current_memory_usage()
            start = time.time()
            result = func(*args, **kwargs)
            elapsed_time = elapsed_since(start)
            mem_after = get_process_memory()
            sys_mem_after = get_current_memory_usage()
            print(
                f"{func_name}: {mem_before=}, {mem_before=}, consumed: {mem_after - mem_before} sys={sys_mem_after -sys_mem_before}; exec time: {elapsed_time}"
            )
            return result

        return wrapper

    return decorator
