@tensorrt_converter(acc_ops.avg_pool2d)
def acc_ops_avg_pool2d(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"AvgPool2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    kernel_size = extend_attr_to_tuple(kwargs["kernel_size"], 2)
    stride = extend_attr_to_tuple(kwargs["stride"], 2)
    padding = extend_attr_to_tuple(kwargs["padding"], 2)
    ceil_mode = kwargs["ceil_mode"]
    count_include_pad = kwargs["count_include_pad"]
    divisor_override = kwargs["divisor_override"]

    if divisor_override:
        raise RuntimeError("TensorRT does not support divisor_override.")

    layer = network.add_pooling(
        input=input_val, type=trt.PoolingType.AVERAGE, window_size=kernel_size
    )
    layer.stride = stride
    layer.padding = padding
    layer.average_count_excludes_padding = False if count_include_pad else True
    set_layer_name(layer, target, name)

    if ceil_mode:
        layer.padding_mode = trt.PaddingMode.EXPLICIT_ROUND_UP

    return layer.get_output(0)
