@register_acc_op
def slice_tensor(*, input, dims, starts, stops, steps):
    slices: List[Optional[slice]] = [None for _ in range(input.dim())]

    # For all provided dims, extract out a slice for starts/stops/steps.
    for idx, dim in enumerate(dims):
        slices[dim] = slice(starts[idx], stops[idx], steps[idx])

    # For all unspecified dims, default to the full slice.
    for idx, s in enumerate(slices):
        if s is None:
            slices[idx] = slice(None, None, None)

    return input[slices]
