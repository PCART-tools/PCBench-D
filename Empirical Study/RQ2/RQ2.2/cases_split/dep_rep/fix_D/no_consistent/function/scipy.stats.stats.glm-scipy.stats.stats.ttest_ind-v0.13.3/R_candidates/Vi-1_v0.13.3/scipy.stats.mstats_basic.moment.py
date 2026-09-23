def moment(a, moment=1, axis=0):
    a, axis = _chk_asarray(a, axis)
    if moment == 1:
        # By definition the first moment about the mean is 0.
        shape = list(a.shape)
        del shape[axis]
        if shape:
            # return an actual array of the appropriate shape
            return np.zeros(shape, dtype=float)
        else:
            # the input was 1D, so return a scalar instead of a rank-0 array
            return np.float64(0.0)
    else:
        mn = ma.expand_dims(a.mean(axis=axis), axis)
        s = ma.power((a-mn), moment)
        return s.mean(axis=axis)
