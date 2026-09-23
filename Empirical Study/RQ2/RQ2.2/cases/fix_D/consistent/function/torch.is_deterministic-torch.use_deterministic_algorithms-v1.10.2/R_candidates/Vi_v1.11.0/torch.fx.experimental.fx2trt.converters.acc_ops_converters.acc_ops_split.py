@tensorrt_converter(acc_ops.split, no_explicit_batch_dim=True)
def acc_ops_split(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"split received input {input_val} that is not part "
                           "of the TensorRT region!")

    dim = cast(int, kwargs["dim"])
    if network.has_implicit_batch_dimension:
        assert dim != 0, "Can't split on batch dim when it's implicit!"
        dim -= 1
    else:
        raise RuntimeError("We don't support split with explicit batch dimension yet!")

    split_size = cast(int, kwargs["split_size"])
    start = [0] * len(input_val.shape)
    stride = [1] * len(start)
    offset = 0
    num_splits = (input_val.shape[dim] + split_size - 1) // split_size
    if num_splits < 1:
        raise RuntimeError(f"Invalid split: {input_val.shape[dim]} with split_size={split_size}")

    max_offset = input_val.shape[dim]
    # add slice layers
    output = []
    for i in range(num_splits):
        shape = list(input_val.shape)
        shape[dim] = min(split_size, cast(int, max_offset - offset))
        start[dim] = offset
        layer = network.add_slice(input_val, start=start, shape=shape, stride=stride)
        offset += split_size
        set_layer_name(layer, target, f"{name}_{i}")
        output.append(layer.get_output(0))
    return output
