@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def slice_tensor(*, input, dim, start, stop, step):
    slc = slice(start, stop, step)
    if dim >= 0:
        slices: List[slice] = [slice(None, None, None) for _ in range(dim)]
        slices.append(slc)
    else:
        slices = [Ellipsis, slc]  # type: ignore[list-item]
        slices.extend([slice(None, None, None) for _ in range(-dim - 1)])

    return input[tuple(slices)]
