def mode(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    def _mode1D(a):
        (rep,cnt) = find_repeats(a)
        if not cnt.ndim:
            return (0, 0)
        elif cnt.size:
            return (rep[cnt.argmax()], cnt.max())
        else:
            not_masked_indices = ma.flatnotmasked_edges(a)
            first_not_masked_index = not_masked_indices[0]
            return (a[first_not_masked_index], 1)

    if axis is None:
        output = _mode1D(ma.ravel(a))
        output = (ma.array(output[0]), ma.array(output[1]))
    else:
        output = ma.apply_along_axis(_mode1D, axis, a)
        newshape = list(a.shape)
        newshape[axis] = 1
        slices = [slice(None)] * output.ndim
        slices[axis] = 0
        modes = output[tuple(slices)].reshape(newshape)
        slices[axis] = 1
        counts = output[tuple(slices)].reshape(newshape)
        output = (modes, counts)
    return output
