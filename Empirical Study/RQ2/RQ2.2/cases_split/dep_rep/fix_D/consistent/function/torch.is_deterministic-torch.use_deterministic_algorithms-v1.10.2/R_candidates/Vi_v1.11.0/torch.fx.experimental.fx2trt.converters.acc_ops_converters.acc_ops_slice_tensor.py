@tensorrt_converter(acc_ops.slice_tensor)
def acc_ops_slice_tensor(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"slice_tensor received input {input_val} that is not part "
                           "of the TensorRT region!")

    ranks = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)
    dim = get_positive_dim(cast(int, kwargs["dim"]), ranks)

    if network.has_implicit_batch_dimension:
        if dim == 0:
            raise RuntimeError(
                f"We do not support slice_tensor at batch dim when it's implicit, got {dim}!"
            )
        dim = dim - 1
    else:
        raise RuntimeError("We don't support slice_tensor with explicit batch dimension yet!")

    start_int = cast(int, kwargs["start"])
    stop_int = cast(int, kwargs["stop"])
    step_int = cast(int, kwargs["step"])
    start = [0] * len(input_val.shape)
    start[dim] = start_int
    stride = [1] * len(start)
    stride[dim] = step_int
    output_shape = list(input_val.shape)
    output_shape[dim] = (stop_int - start_int) // step_int

    layer = network.add_slice(input_val, start=start, shape=output_shape, stride=stride)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
