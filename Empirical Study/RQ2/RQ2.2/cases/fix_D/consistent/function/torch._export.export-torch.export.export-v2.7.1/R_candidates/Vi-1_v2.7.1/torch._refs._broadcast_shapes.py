def _broadcast_shapes(*_shapes):
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    shapes = tuple(
        (x,) if isinstance(x, IntLike) else x
        for x in filter(lambda x: x is not None, _shapes)
    )

    # Short-circuits on no input
    if len(shapes) == 0:
        return None

    # Type checking
    # TODO: make common validations available as utils
    for shape in shapes:
        assert isinstance(shape, Sequence)

    # Computes common shape
    common_shape: list[Union[int, torch.SymInt]] = [
        1,
    ] * reduce(max, (len(shape) for shape in shapes))
    for arg_idx, shape in enumerate(shapes):
        for idx in range(-1, -1 - len(shape), -1):
            if guard_size_oblivious(common_shape[idx] == 1):
                if shape[idx] < 0:
                    raise ValueError(
                        "Attempting to broadcast a dimension with negative length!"
                    )
                common_shape[idx] = shape[idx]
            elif guard_size_oblivious(shape[idx] != 1):
                torch._check(
                    common_shape[idx] == shape[idx],
                    lambda: f"Attempting to broadcast a dimension of length {shape[idx]} at {idx}! "
                    f"Mismatching argument at index {arg_idx} had {shape}; but expected shape "
                    f"should be broadcastable to {common_shape}",
                )

    return common_shape
