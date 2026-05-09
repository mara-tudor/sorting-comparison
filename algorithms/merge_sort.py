def merge_sort(arr):
    """
    Merge Sort — O(n log n) in all cases.
    Stable, requires O(n) auxiliary space.
    """
    a = arr[:]
    _merge_sort(a, 0, len(a) - 1)
    return a


def _merge_sort(a, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    _merge_sort(a, left, mid)
    _merge_sort(a, mid + 1, right)
    _merge(a, left, mid, right)


def _merge(a, left, mid, right):
    L = a[left : mid + 1]
    R = a[mid + 1 : right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            a[k] = L[i]
            i += 1
        else:
            a[k] = R[j]
            j += 1
        k += 1
    while i < len(L):
        a[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        a[k] = R[j]
        j += 1
        k += 1
