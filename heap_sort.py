def heap_sort(arr):
    """
    Heap Sort — O(n log n) in all cases.
    Not stable, in-place (O(1) extra space).
    """
    a = arr[:]
    n = len(a)

    # Build max-heap using Floyd's algorithm
    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]   # move current max to end
        _heapify(a, i, 0)

    return a


def _heapify(a, n, i):
    """Maintain max-heap property rooted at index i, heap size n."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and a[left] > a[largest]:
        largest = left
    if right < n and a[right] > a[largest]:
        largest = right

    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        _heapify(a, n, largest)
