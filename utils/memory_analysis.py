import tracemalloc


def analyze_memory(function, data):

    tracemalloc.start()

    function(data.copy())

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {

        "current_memory": current,

        "peak_memory": peak

    }