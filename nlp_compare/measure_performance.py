import psutil
import time
from functools import wraps


def measure_performance_(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Record start time and CPU usage
        start_time = time.time()
        start_cpu_times = psutil.cpu_times_percent(interval=None)

        result = func(*args, **kwargs)

        # Record end time and CPU usage
        end_time = time.time()
        end_cpu_times = psutil.cpu_times_percent(interval=None)

        # Calculate elapsed time and CPU usage
        elapsed_time = end_time - start_time
        cpu_usage = {
            "user": end_cpu_times.user - start_cpu_times.user,
            "system": end_cpu_times.system - start_cpu_times.system,
            "idle": end_cpu_times.idle - start_cpu_times.idle,
        }

        print(f"Function '{func.__name__}' executed in {elapsed_time:.2f} seconds")
        print(f"CPU usage: {cpu_usage}")

        return result

    return wrapper


def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Record start time and CPU usage
        start_time = time.time()
        process = psutil.Process()
        start_cpu_times = process.cpu_times()

        result = func(*args, **kwargs)

        # Record end time and CPU usage
        end_time = time.time()
        end_cpu_times = process.cpu_times()

        # Calculate elapsed time and CPU usage
        elapsed_time = end_time - start_time
        cpu_usage = {
            "user": end_cpu_times.user - start_cpu_times.user,
            "system": end_cpu_times.system - start_cpu_times.system,
        }

        print(f"Function '{func.__name__}' executed in {elapsed_time:.3f} seconds")
        print(f"CPU usage: {cpu_usage}")

        return result

    return wrapper
