import time
import statistics


def benchmark_algorithm(function, data, runs=100):

    execution_times = []

    for _ in range(runs):

        copied_data = data.copy()

        start = time.perf_counter()

        function(copied_data)

        end = time.perf_counter()

        execution_times.append(end - start)

    return {

        "average": statistics.mean(execution_times),

        "minimum": min(execution_times),

        "maximum": max(execution_times),

        "std_dev": statistics.stdev(execution_times)

    }