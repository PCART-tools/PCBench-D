def _wrapped_qr(a):
    """
    A wrapper for np.linalg.qr that handles arrays with 0 rows

    Notes: Created for tsqr so as to manage cases with uncertain
    array dimensions. In particular, the case where arrays have
    (uncertain) chunks with 0 rows.
    """
    # workaround may be removed when numpy stops rejecting edge cases
    if a.shape[0] == 0:
        return np.zeros((0, 0)), np.zeros((0, a.shape[1]))
    else:
        return np.linalg.qr(a)
