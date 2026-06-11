def linear_search(arr, target):

    comparisons = 0

    for index, value in enumerate(arr):

        comparisons += 1

        if value == target:
            return index, comparisons

    return -1, comparisons


def binary_search(arr, target):

    low = 0
    high = len(arr) - 1

    comparisons = 0

    while low <= high:

        comparisons += 1

        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons

        elif arr[mid] < target:
            low = mid + 1

        else:
            high = mid - 1

    return -1, comparisons