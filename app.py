from flask import Flask, render_template, request
import time

from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort
)

from algorithms.searching import (
    linear_search,
    binary_search
)

from utils.benchmark import benchmark_algorithm
from utils.memory_analysis import analyze_memory
from utils.complexity import complexity_data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    sorting_results = {}
    searching_results = {}

    fastest_algorithm = None
    lowest_memory_algorithm = None

    if request.method == "POST":

        numbers = list(map(int, request.form["numbers"].split(",")))

        target = request.form.get("target")

        sorting_algorithms = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort
        }

        # SORTING ANALYSIS
        for name, algorithm in sorting_algorithms.items():

            start = time.perf_counter()

            sorted_array = algorithm(numbers.copy())

            execution_time = time.perf_counter() - start

            benchmark = benchmark_algorithm(algorithm, numbers)

            memory = analyze_memory(algorithm, numbers)

            sorting_results[name] = {
                "sorted_array": sorted_array,
                "execution_time": execution_time,
                "average_time": benchmark["average"],
                "minimum_time": benchmark["minimum"],
                "maximum_time": benchmark["maximum"],
                "std_dev": benchmark["std_dev"],
                "peak_memory": memory["peak_memory"]
            }

        # Fastest sorting algorithm
        fastest_algorithm = min(
            sorting_results,
            key=lambda x: sorting_results[x]["average_time"]
        )

        # Lowest memory algorithm
        lowest_memory_algorithm = min(
            sorting_results,
            key=lambda x: sorting_results[x]["peak_memory"]
        )

        # SEARCHING ANALYSIS
        if target:

            target = int(target)

            # Binary search requires sorted array
            sorted_numbers = sorted(numbers)

            search_algorithms = {
                "Linear Search": (
                    numbers,
                    linear_search
                ),

                "Binary Search": (
                    sorted_numbers,
                    binary_search
                )
            }

            for name, (data, algorithm) in search_algorithms.items():

                start = time.perf_counter()

                index_found, comparisons = algorithm(data, target)

                execution_time = time.perf_counter() - start

                searching_results[name] = {
                    "index": index_found,
                    "comparisons": comparisons,
                    "execution_time": execution_time
                }

    return render_template(
        "index.html",

        sorting_results=sorting_results,

        searching_results=searching_results,

        fastest_algorithm=fastest_algorithm,

        lowest_memory_algorithm=lowest_memory_algorithm,

        complexity_data=complexity_data
    )


if __name__ == "__main__":
    app.run(debug=True)