def _finalize_nsmallest(arr, kth_val, n, take_last, narr):
    ns, = np.nonzero(arr <= kth_val)
    inds = ns[arr[ns].argsort(kind='mergesort')][:n]

    if take_last:
        # reverse indices
        return narr - 1 - inds
    return inds
