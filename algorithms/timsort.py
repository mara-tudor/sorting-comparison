def timsort(arr):
    """
    Python's built-in sorted() function (C implementation).
    
    Note: This is NOT a hand-written Python implementation of Timsort.
    It is included as a C-level reference baseline only to show the performance
    gap between pure Python and compiled C implementations.
    The underlying algorithm in CPython 3.11+ uses a modern merge-insertion hybrid
    strategy rather than the original Timsort from Peters 2002.
    
    Included for educational comparison only; should not be evaluated on equal
    terms with the other hand-written Python sorting algorithms.
    """
    return sorted(arr)
