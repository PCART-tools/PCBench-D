def _broadcast_in_dim_meta(
    a: TensorLikeType, shape: ShapeType, broadcast_dimensions: Sequence[int]
):
    from torch.fx.experimental.symbolic_shapes import (
        guard_or_false,
        guard_or_true,
        sym_or,
    )

    # Type checks
    assert isinstance(a, TensorLike)
    assert isinstance(shape, Sequence)
    assert isinstance(broadcast_dimensions, Sequence)

    # every dimension must be accounted for
    assert a.ndim == len(broadcast_dimensions)

    # broadcast shape must have weakly more dimensions
    assert len(shape) >= a.ndim

    # broadcast_dimensions must be an ascending sequence
    # (no relative reordering of dims) of integers and
    # each dimension must be within the new shape
    def _greater_than_reduce(acc, x):
        assert isinstance(x, Dim)
        assert x > acc
        assert x < len(shape)

        return x

    reduce(_greater_than_reduce, broadcast_dimensions, -1)

    # shape must be broadcastable to
    for idx, new_idx in enumerate(broadcast_dimensions):
        torch._check(
            sym_or(a.shape[idx] == 1, shape[new_idx] == a.shape[idx]),
            lambda: f"{a.shape[idx]} must be broadcastable to {shape[new_idx]}",
        )

    new_strides = []
    original_idx = 0
    for idx in range(len(shape)):
        if idx in broadcast_dimensions:
            # Assigns a stride of zero to dimensions
            # which were actually broadcast
            if guard_or_false(a.shape[original_idx] == 1):
                if guard_or_false(a.shape[original_idx] == shape[idx]):
                    new_strides.append(a.stride()[original_idx])
                else:
                    new_strides.append(0)
            else:
                torch._check(
                    a.shape[original_idx] == shape[idx],
                    lambda: f"non-broadcasting semantics require {a.shape[original_idx]} == {shape[idx]}",
                )
                new_strides.append(a.stride()[original_idx])
            original_idx = original_idx + 1
        else:
            if guard_or_true(shape[idx] != 1):
                # consistent with previous use of guard_size_oblivious
                new_strides.append(0)
            elif original_idx == a.ndim:
                new_strides.append(1)
            else:
                new_strides.append(a.stride()[original_idx] * a.size()[original_idx])

    return a.as_strided(shape, new_strides, a.storage_offset())
