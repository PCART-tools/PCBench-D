@tensorrt_converter(acc_ops.pad, enabled=trt.__version__ >= "8.2")
def acc_ops_pad_with_slice_layer(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    pad = cast(Sequence[int], kwargs["pad"])
    mode = kwargs["mode"]
    value = kwargs["value"]
    rank = len(input_val.shape)  # type: ignore[union-attr]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"pad received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if mode != "constant":
        raise RuntimeError(
            f"Currently we only support constant mode for pad, got {mode}."
        )

    if len(pad) / 2 > rank:
        raise RuntimeError(
            f"Trying to pad last {len(pad) / 2} dimension but the input only has {rank} dimension."
        )

    if value != 0:
        raise RuntimeError(
            f"Currently we only support padding value of 0, got {value}."
        )

    input_shape = input_val.shape
    pre_start = tuple(i - 1 for i in input_shape)
    prefix_len = len(input_shape) - len(pad) // 2
    pre_shape = tuple(input_shape[i] + (pad[-(i - prefix_len) * 2 - 2] if i >= prefix_len else 0)
                      for i in range(0, len(input_shape)))
    pre_stride = [-1] * len(input_shape)

    layer = network.add_slice(
        input_val,
        pre_start,
        pre_shape,
        pre_stride,
    )
    layer.mode = trt.SliceMode.FILL
    set_layer_name(layer, target, f"pre_{name}")
    half_pad_output = layer.get_output(0)

    shape = half_pad_output.shape
    mid_start = tuple(i - 1 for i in shape)
    mid_stride = [-1] * len(shape)
    layer = network.add_slice(
        half_pad_output,
        mid_start,
        shape,
        mid_stride
    )
    layer.mode = trt.SliceMode.FILL
    set_layer_name(layer, target, f"transpose_{name}")
    transpose_output = layer.get_output(0)

    shape = transpose_output.shape
    post_start = tuple([0] * len(shape))
    post_shape = tuple(
        shape[i] + (pad[-(i - prefix_len) * 2 - 1] if i >= prefix_len else 0) for i in range(0, len(shape))
    )
    post_stride = tuple([1] * len(shape))

    layer = network.add_slice(
        transpose_output,
        post_start,
        post_shape,
        post_stride
    )
    layer.mode = trt.SliceMode.FILL
    set_layer_name(layer, target, f"post_{name}")
    return layer.get_output(0)
