@tensorrt_converter(acc_ops.sum)
def acc_ops_sum(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"sum received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    # If dim is specified, then we are computing reduced sum over certain dimensions.
    # Otherwise, we are dong summation over all elements, which is only supported in
    # explicit batch dimension.
    if "dim" not in kwargs:
        assert (
            not network.has_implicit_batch_dimension
        ), "Do not support sum all the elements for implicit batch."
        dim = range(0, len(input_val.shape))
    else:
        dim = kwargs["dim"]

    keepdim = False if "keepdim" not in kwargs else kwargs["keepdim"]
    layer = network.add_reduce(
        input_val,
        trt.ReduceOperation.SUM,
        get_axes_for_reduce_op(dim, network.has_implicit_batch_dimension),
        keepdim,
    )
    layer.name = name
    return layer.get_output(0)
