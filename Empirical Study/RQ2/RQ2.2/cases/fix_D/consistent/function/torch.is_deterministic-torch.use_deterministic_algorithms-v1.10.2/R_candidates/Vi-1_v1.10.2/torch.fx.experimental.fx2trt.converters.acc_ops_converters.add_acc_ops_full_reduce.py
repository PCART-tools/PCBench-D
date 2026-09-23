def add_acc_ops_full_reduce(network, target, args, kwargs, name, reduce_op):
    input_val = kwargs["input"]
    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"max received input {input_val} that is not part "
            "of the TensorRT region!"
        )
    assert (
        not network.has_implicit_batch_dimension
    ), "Do not support max over all the elements for implicit batch."

    dim = range(len(input_val.shape))

    layer = network.add_reduce(
        input_val,
        reduce_op,
        get_axes_for_reduce_op(dim, network.has_implicit_batch_dimension),
        False,
    )
    layer.name = name
    return layer.get_output(0)
