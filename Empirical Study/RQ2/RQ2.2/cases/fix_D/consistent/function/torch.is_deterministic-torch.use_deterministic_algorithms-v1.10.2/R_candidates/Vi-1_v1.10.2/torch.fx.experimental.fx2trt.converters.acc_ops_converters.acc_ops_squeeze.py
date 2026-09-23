@tensorrt_converter(acc_ops.squeeze)
def acc_ops_squeeze(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"squeeze received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    dim = kwargs["dim"] if "dim" in kwargs else None
    # Squeeze with dim=None would only work in explicit batch dim mode without any dynamic
    # dim, which is a very rare case. For now we just claim not supporting dim=None.
    assert dim is not None, "We don't support dim=None right now."

    dim = dim % (len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0))
    if network.has_implicit_batch_dimension:
        assert dim != 0, "We don't support squeeze batch dim when it's implicit."
        dim -= 1

    assert input_val.shape[dim] != -1, "We don't support squeeze dynamic dim."
    assert (
        len(get_dynamic_dims(input_val.shape)) <= 1
    ), "Currently more than one dynamic dim for input to squeeze is not supported."

    output_shape = []
    for i, s in enumerate(input_val.shape):
        if i == dim and s == 1:
            continue
        output_shape.append(s)
    layer = network.add_shuffle(input_val)
    layer.reshape_dims = tuple(output_shape)
    layer.name = name
    return layer.get_output(0)
