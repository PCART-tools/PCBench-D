def compute_stderr(a, axis=0, ddof=1):
    a, axis = _chk_asarray(a, axis)
    return np.std(a,axis,ddof=1) / float(np.sqrt(a.shape[axis]))
