@tensorrt_converter(acc_ops.slice_tensor)
def acc_ops_slice_tensor(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"slice_tensor received input {input_val} that is not part "
                           "of the TensorRT region!")

    dims = kwargs["dims"]
    if network.has_implicit_batch_dimension:
        if not len(dims):
            raise RuntimeError("dim argument cannot be empty!")
        if any([dim == 0 for dim in dims]):
            raise RuntimeError(
                f"We do not support slice_tensor at batch dim when it's implicit, got {dims}!"
            )
        dims = [d - 1 for d in dims]
    else:
        raise RuntimeError("We don't support slice_tensor with explicit batch dimension yet!")

    start = [0] * len(input_val.shape)
    stride = [1] * len(start)
    output_shape = list(input_val.shape)
    starts = kwargs["starts"]
    stops = kwargs["stops"]
    steps = kwargs["steps"]

    for i, dim in enumerate(dims):
        start[dim] = starts[i]
        stride[dim] = steps[i]
        output_shape[dim] = (stops[i] - start[i]) // steps[i]

    layer = network.add_slice(input_val, start=start, shape=output_shape, stride=stride)
    layer.name = name
    return layer.get_output(0)
