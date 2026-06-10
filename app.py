from flask import Flask, render_template, request
import time

app = Flask(__name__)

# Insertion Sort
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

def bubble_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0

    n = len(a)

    for i in range(n):
        for j in range(0, n-i-1):
            comparisons += 1

            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1

    return a, comparisons, swaps

def selection_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(a)):
        min_idx = i

        for j in range(i+1, len(a)):
            comparisons += 1

            if a[j] < a[min_idx]:
                min_idx = j

        a[i], a[min_idx] = a[min_idx], a[i]
        swaps += 1

    return a, comparisons, swaps

def merge_sort(arr):

    comparisons = [0]

    def sort(a):

        if len(a) <= 1:
            return a

        mid = len(a)//2

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

# Quick Sort
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

    result = sort(arr.copy())
    return result, comparisons[0]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            numbers = request.form["numbers"]

            arr = [int(x.strip()) for x in numbers.split(",")]

            start = time.time()
            insertion_result, insertion_comp, insertion_swaps = insertion_sort(arr)
            insertion_time = time.time() - start

            start = time.time()
            quick_result, quick_comp = quick_sort(arr)
            quick_time = time.time() - start

            winner = (
                "Insertion Sort"
                if insertion_time < quick_time
                else "Quick Sort"
            )

            return render_template(
                "index.html",
                original_array=arr,
                sorted_array=quick_result,
                insertion_time=round(insertion_time, 8),
                quick_time=round(quick_time, 8),
                insertion_comp=insertion_comp,
                insertion_swaps=insertion_swaps,
                quick_comp=quick_comp,
                winner=winner,
                total=len(arr)
            )

        except ValueError:
            return render_template(
                "index.html",
                error="Enter valid integers separated by commas."
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)