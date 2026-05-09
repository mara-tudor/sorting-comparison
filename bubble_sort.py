def bubble_sort(arr):
    """
    Bubble Sort — O(n^2) average/worst, O(n) best (early-exit optimisation).
    Stable, in-place.
    """
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break  # already sorted — early exit
    return a
