def broadcast(network, a, b, a_name, b_name, preset_diff=0):
    """
    Broadcast two TensorRT tensors to the same number of dimensions by
    prepending 1s to the tensor with less number of dimensions.

    Args:
        network: TensorRT network object.
        a: A TensorRT tensor.
        b: A TensorRT tensor.
        a_name: Name of tensor a.
        b_name: Name of tensor b.
        preset_diff: The difference of number of dimensions after broadcast.
            A positive number means after broadcast, tensor `a` would have
            `preset_diff` more dimensions than `b`. This is used in matmul,
            since we need to broadcast tensors but not always to the same
            number of dimension. The reason is that matmul supports Matrix
            x Vector and in this case broadcasted vector should have 1 less
            number of dimensions than the matrix tensor.
    """
    a_shape = tuple(a.shape)
    b_shape = tuple(b.shape)

    diff = len(a_shape) - len(b_shape) - preset_diff
    if diff > 0:
        b = append_ones(network, b, f"{b_name}_broadcast", diff)
    elif diff < 0:
        a = append_ones(network, a, f"{a_name}_broadcast", -diff)

    return a, b
