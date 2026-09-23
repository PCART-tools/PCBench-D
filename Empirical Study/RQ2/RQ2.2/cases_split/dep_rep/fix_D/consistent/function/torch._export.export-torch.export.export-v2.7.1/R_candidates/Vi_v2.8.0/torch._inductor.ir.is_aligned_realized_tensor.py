def is_aligned_realized_tensor(x: Union[Buffer, TensorBox], alignment: int) -> bool:
    if not isinstance(x, IRNode) or x.maybe_get_stride() is None:
        return False

    aligned_strides = all(
        (V.graph.sizevars.size_hint_or_throw(x.get_stride()[i]) % alignment) == 0
        for i in range(len(x.get_stride()) - 1)
    )
    # if the last dim size is <= 1, stride doesn't matter
    aligned_last_dim = (
        V.graph.sizevars.size_hint_or_throw(x.get_stride()[-1]) == 1
        or V.graph.sizevars.size_hint_or_throw(x.get_size()[-1]) <= 1
    )
    return aligned_last_dim and aligned_strides
