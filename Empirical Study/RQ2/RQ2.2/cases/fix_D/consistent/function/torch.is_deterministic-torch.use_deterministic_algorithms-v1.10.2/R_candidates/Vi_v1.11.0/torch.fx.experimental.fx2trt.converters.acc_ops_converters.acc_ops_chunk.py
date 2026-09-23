@tensorrt_converter(acc_ops.chunk)
def acc_ops_chunk(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    chunks = cast(int, kwargs["chunks"])
    dim = cast(int, kwargs["dim"])
    input_dim_size = len(input_val.shape)  # type: ignore[union-attr]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"chunk received input {input_val} that is not part "
                           "of the TensorRT region!")

    if network.has_implicit_batch_dimension:
        input_dim_size += 1
        dim = get_positive_dim(dim, input_dim_size)
        assert dim != 0, "Can't chunk on batch dim when it's implicit!"
        dim -= 1
    else:
        assert not has_dynamic_shape(input_val.shape), "We currently don't support dynamic shape for chunk."
        dim = get_positive_dim(dim, input_dim_size)

    if chunks > input_val.shape[dim]:
        warnings.warn(
            f"Asked for {chunks} chunks along dimention "
            f"{dim} on tensor with size {input_val.shape}, chunks "
            f"will default to {input_val.shape[dim]}",
            RuntimeWarning
        )
        chunks = input_val.shape[dim]

    start = [0] * len(input_val.shape)
    stride = [1] * len(start)
    offset = 0
    split_size = (input_val.shape[dim] + chunks - 1) // chunks

    max_offset = input_val.shape[dim]
    # add slice layers
    output = []
    for i in range(chunks):
        shape = list(input_val.shape)
        shape[dim] = min(split_size, max_offset - offset)
        start[dim] = offset
        layer = network.add_slice(input_val, start=start, shape=shape, stride=stride)
        offset += split_size
        set_layer_name(layer, target, f"{name}_{i}")
        output.append(layer.get_output(0))
    return output
