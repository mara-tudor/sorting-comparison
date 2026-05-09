def timsort(arr):
    """
    Timsort — Python's built-in sorting algorithm (Tim Peters, 2002).
    Hybrid of Merge Sort and Insertion Sort; exploits existing order (runs).
    O(n log n) worst case, O(n) best case (already sorted).
    Stable, requires O(n) auxiliary space.

    We wrap Python's built-in sorted() so Timsort fits the same interface
    as the other algorithms in this benchmark.
    """
    return sorted(arr)
