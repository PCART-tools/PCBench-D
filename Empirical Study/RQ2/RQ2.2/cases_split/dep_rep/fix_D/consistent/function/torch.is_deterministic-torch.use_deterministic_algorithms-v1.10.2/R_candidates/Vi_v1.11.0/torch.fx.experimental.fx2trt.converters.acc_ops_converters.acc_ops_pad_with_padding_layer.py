@tensorrt_converter(acc_ops.pad, enabled=trt.__version__ < "8.2")
def acc_ops_pad_with_padding_layer(
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

    if len(pad) > 4:
        raise RuntimeError("Currently we only support padding last two dimensions.")

    pre_padding = tuple(pad[len(pad) - i - 2] for i in range(0, len(pad), 2))
    post_padding = tuple(pad[len(pad) - i - 1] for i in range(0, len(pad), 2))

    layer = network.add_padding(
        input_val,
        pre_padding if len(pre_padding) == 2 else (0,) + pre_padding,
        post_padding if len(post_padding) == 2 else (0,) + post_padding
    )
    set_layer_name(layer, target, name)
    return layer.get_output(0)
