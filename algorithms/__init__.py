from .insertion_sort import insertion_sort
from .selection_sort import selection_sort
from .bubble_sort import bubble_sort
from .merge_sort import merge_sort
from .quicksort import quicksort
from .heap_sort import heap_sort
from .timsort import timsort

ALL_ALGORITHMS = {
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Bubble Sort":    bubble_sort,
    "Merge Sort":     merge_sort,
    "Quicksort":      quicksort,
    "Heap Sort":      heap_sort,
    "Timsort":        timsort,
}
