def infer_dense_strides(size: Sequence[int], orig_strides: Sequence[int]):
    """This is a mirror of the same function in aten/src/ATen/ExpandUtils.cpp

    Args:
        size: The size of the output tensor
        orig_strides: The strides of the input tensor
    Returns:
        List[int]: Dense non-overlapping strides that preserve the input tensor's layout permutation.
        The returned strides follow the same stride propagation rules as TensorIterator. This matches
        The behavior of empty_like()
    """
    fill_order = get_fill_order(orig_strides, V.graph.sizevars.shape_env)
    return construct_strides(size, fill_order)
