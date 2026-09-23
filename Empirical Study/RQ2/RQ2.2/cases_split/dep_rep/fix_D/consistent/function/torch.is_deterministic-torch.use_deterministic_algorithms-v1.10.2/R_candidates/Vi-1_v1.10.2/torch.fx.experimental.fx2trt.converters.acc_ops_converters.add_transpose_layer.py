def add_transpose_layer(
    network, input_val, dim_0, dim_1, name, ignore_implicit_batch=False
):
    """Adds a transpose layer to the TensorRT network
    Args:
        network: TensorRT Network object
        input_val: tensorrt.ITensor
        dim_0, dim_1: dimensions for transpose, e.g. dim_0=1, dim_1=0 means transpose
        the first two dimensions
        name: Name of the layer
        ignore_implicit_batch: activations might have implicit batch, but weights do
        not, when this is True, we'll ignore the implicit batch and use the dimension
        argument as is
    Returns:
        output TensorRT ITensor from the transpose layer
    """
    if not ignore_implicit_batch and network.has_implicit_batch_dimension:
        assert (
            dim_0 != 0 and dim_1 != 0
        ), "It's not allowed to call transpose on non-constant when batch dim is implicit!"
        dim_0 -= 1
        dim_1 -= 1

    permutation = list(range(len(input_val.shape)))
    permutation[dim_0] = dim_1
    permutation[dim_1] = dim_0

    layer = network.add_shuffle(input_val)
    layer.second_transpose = tuple(permutation)
    layer.name = name
    return layer.get_output(0)
