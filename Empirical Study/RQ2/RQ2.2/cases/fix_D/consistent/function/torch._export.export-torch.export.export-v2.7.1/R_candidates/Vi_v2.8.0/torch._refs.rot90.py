@register_decomposition(aten.rot90)
@out_wrapper()
def rot90(
    a: TensorLikeType, k: int = 1, dims: DimsSequenceType = (0, 1)
) -> TensorLikeType:
    """Reference implementation of :func:`torch.rot90`."""
    if len(dims) != 2:
        raise RuntimeError(
            f"expected total rotation dims == 2, but got dims = {len(dims)}"
        )
    if a.ndim < 2:
        raise RuntimeError(f"expected total dims >= 2, but got total dims = {a.ndim}")

    # Do this after the initial checks to be compatible with the behavior in
    # core.
    dims = utils.canonicalize_dims(a.ndim, dims)

    if dims[0] == dims[1]:
        raise RuntimeError(
            f"expected rotation dims to be different, but got dim0 = {dims[0]} and dim1 = {dims[1]}"
        )
    k = k % 4  # Rotation direction is from the second towards the first axis for k < 0
    if k == 1:
        return torch.transpose(torch.flip(a, (dims[1],)), dims[0], dims[1])
    elif k == 2:
        return torch.flip(a, dims)
    elif k == 3:
        return torch.transpose(torch.flip(a, (dims[0],)), dims[0], dims[1])
    else:
        return a.clone(memory_format=torch.contiguous_format)
