def get_axes_for_reduce_op(
    dim: Union[int, Sequence[int]],
    has_implicit_batch_dimension: bool,
) -> int:
    """
    TensorRT reduce layer relies on the binary representation of axes to
    determine which dims to reduce. For example, if we want to reduce on
    dim 1 and 2 then axes should be 6(110).

    Args:
        dim (Union[int, Sequence[int]]): An integer or a sequence of integers
            that will be used to generate axes for TensorRT.
        has_implicit_batch_dimension (bool): Whether the TensorRT network is
            using implicit batch dimension.

    Returns:
        An integer which binary form can be used as axes for TensorRT reduce
        layer.
    """
    if isinstance(dim, int):
        dim = (dim,)

    if has_implicit_batch_dimension:
        assert 0 not in dim, "Can't reduce over batch dimension when it's implicit."

    axes = 0
    for d in dim:
        axes |= 1 << (d - (1 if has_implicit_batch_dimension else 0))

    return axes
