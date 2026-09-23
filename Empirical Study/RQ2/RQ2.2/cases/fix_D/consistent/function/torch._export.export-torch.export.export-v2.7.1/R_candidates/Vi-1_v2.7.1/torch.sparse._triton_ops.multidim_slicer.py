def multidim_slicer(dims, slices, *tensors):
    for t in tensors:
        s = [slice(None)] * t.dim()
        for d, d_slice in zip(dims, slices):
            if d is not None:
                s[d] = d_slice
        yield t[s]
