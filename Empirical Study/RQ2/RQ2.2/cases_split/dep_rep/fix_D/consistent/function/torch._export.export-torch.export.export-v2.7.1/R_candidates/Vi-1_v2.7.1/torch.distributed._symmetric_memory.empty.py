def empty(  # type: ignore[misc]
    *size: Any,
    dtype: Optional[_dtype] = None,
    device: Optional[_device] = None,
) -> torch.Tensor:
    r"""
    empty(*size, *, dtype=None, device=None) -> Tensor

    Similar to :func:`torch.empty()`. The returned tensor can be used by
    :func:`torch._distributed._symmetric_memory.rendezvous()` to establish a
    symmetric memory tensor among participating processes.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).
        device (:class:`torch.device`, optional): the desired device of returned tensor.
            Default: if ``None``, uses the current device for the default tensor type
            (see :func:`torch.set_default_device`). :attr:`device` will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    """
    if len(size) == 1 and isinstance(size[0], Sequence):
        size = tuple(size[0])
    else:
        size = tuple(size)

    if dtype is None:
        dtype = torch.get_default_dtype()

    if device is None:
        device = torch.get_default_device()

    return _SymmetricMemory.empty_strided_p2p(
        size=size,
        stride=torch._prims_common.make_contiguous_strides_for(size),
        dtype=dtype,
        device=torch.device(device),
    )
