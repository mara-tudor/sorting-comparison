def quicksort(arr):
    """
    Quicksort with median-of-three pivot selection.
    O(n log n) average, O(n^2) worst case (rare with MoT).
    Not stable, in-place (O(log n) stack space).
    """
    a = arr[:]
    _quicksort(a, 0, len(a) - 1)
    return a


def _median_of_three(a, low, high):
    mid = (low + high) // 2
    # Sort low, mid, high positions so median ends up at mid
    if a[low] > a[mid]:
        a[low], a[mid] = a[mid], a[low]
    if a[low] > a[high]:
        a[low], a[high] = a[high], a[low]
    if a[mid] > a[high]:
        a[mid], a[high] = a[high], a[mid]
    # Place pivot (median) just before high
    a[mid], a[high - 1] = a[high - 1], a[mid]
    return a[high - 1]


def _quicksort(a, low, high):
    if high - low < 2:
        # Base case: 0 or 1 element — already sorted
        if high > low and a[low] > a[high]:
            a[low], a[high] = a[high], a[low]
        return

    pivot = _median_of_three(a, low, high)
    i = low
    j = high - 1

    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            break
        a[i], a[j] = a[j], a[i]

    # Restore pivot
    a[i], a[high - 1] = a[high - 1], a[i]

    _quicksort(a, low, i - 1)
    _quicksort(a, i + 1, high)
