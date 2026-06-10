from flask import Flask, render_template, request
import time

app = Flask(__name__)

# ---------------- INSERTION SORT ----------------
def insertion_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break

        a[j + 1] = key

    return a, comparisons, swaps


# ---------------- BUBBLE SORT ----------------
def bubble_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0

    n = len(a)

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1

    return a, comparisons, swaps


# ---------------- SELECTION SORT ----------------
def selection_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(a)):
        min_idx = i

        for j in range(i + 1, len(a)):
            comparisons += 1

            if a[j] < a[min_idx]:
                min_idx = j

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, comparisons, swaps


# ---------------- MERGE SORT ----------------
def merge_sort(arr):
    comparisons = [0]

    def sort(a):
        if len(a) <= 1:
            return a

        mid = len(a) // 2

        left = sort(a[:mid])
        right = sort(a[mid:])

        result = []

        i = j = 0

        while i < len(left) and j < len(right):
            comparisons[0] += 1

            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    return sort(arr.copy()), comparisons[0]


# ---------------- QUICK SORT ----------------
def quick_sort(arr):
    comparisons = [0]

    def sort(a):
        if len(a) <= 1:
            return a

        pivot = a[len(a) // 2]

        left = []
        middle = []
        right = []

        for x in a:
            comparisons[0] += 1

            if x < pivot:
                left.append(x)
            elif x > pivot:
                right.append(x)
            else:
                middle.append(x)

        return sort(left) + middle + sort(right)

    return sort(arr.copy()), comparisons[0]


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        try:
            numbers = request.form["numbers"]
            arr = [int(x.strip()) for x in numbers.split(",")]

            # Insertion Sort
            start = time.perf_counter()
            insertion_result, insertion_comp, insertion_swaps = insertion_sort(arr)
            insertion_time = time.perf_counter() - start

            # Bubble Sort
            start = time.perf_counter()
            bubble_result, bubble_comp, bubble_swaps = bubble_sort(arr)
            bubble_time = time.perf_counter() - start

            # Selection Sort
            start = time.perf_counter()
            selection_result, selection_comp, selection_swaps = selection_sort(arr)
            selection_time = time.perf_counter() - start

            # Merge Sort
            start = time.perf_counter()
            merge_result, merge_comp = merge_sort(arr)
            merge_time = time.perf_counter() - start

            # Quick Sort
            start = time.perf_counter()
            quick_result, quick_comp = quick_sort(arr)
            quick_time = time.perf_counter() - start

            times = {
                "Insertion Sort": insertion_time,
                "Bubble Sort": bubble_time,
                "Selection Sort": selection_time,
                "Merge Sort": merge_time,
                "Quick Sort": quick_time
            }

            winner = min(times, key=times.get)

            return render_template(
                "index.html",
                original_array=arr,
                sorted_array=quick_result,
                winner=winner,
                total=len(arr),

                insertion_time=round(insertion_time, 8),
                insertion_comp=insertion_comp,
                insertion_swaps=insertion_swaps,

                bubble_time=round(bubble_time, 8),
                bubble_comp=bubble_comp,
                bubble_swaps=bubble_swaps,

                selection_time=round(selection_time, 8),
                selection_comp=selection_comp,
                selection_swaps=selection_swaps,

                merge_time=round(merge_time, 8),
                merge_comp=merge_comp,

                quick_time=round(quick_time, 8),
                quick_comp=quick_comp
            )

        except ValueError:
            return render_template(
                "index.html",
                error="Please enter valid integers separated by commas."
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)