def _finalize_nsmallest(arr, kth_val, n, keep, narr):
    ns, = np.nonzero(arr <= kth_val)
    inds = ns[arr[ns].argsort(kind='mergesort')][:n]
    if keep == 'last':
        # reverse indices
        return narr - 1 - inds
    else:
        return inds
