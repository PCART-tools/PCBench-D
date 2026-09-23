@tensorrt_converter(acc_ops.batch_norm)
def acc_ops_batch_norm(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"BatchNorm2d received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if has_dynamic_shape(input_val.shape):
        assert input_val.shape[1] != -1, "Channel dim can't be dynamic for batch norm."

    scale = cast(torch.Tensor, to_numpy(cast(torch.Tensor, kwargs["weight"]))) / np.sqrt(
        cast(torch.Tensor, to_numpy(cast(torch.Tensor, kwargs["running_var"]))) + cast(float, kwargs["eps"])
    )

    bias = (
        to_numpy(cast(torch.Tensor, kwargs["bias"]))
        - to_numpy(cast(torch.Tensor, kwargs["running_mean"])) * scale
    )
    power = np.ones_like(scale)

    layer = network.add_scale(input_val, trt.ScaleMode.CHANNEL, bias, scale, power)
    set_layer_name(layer, target, name)

    return layer.get_output(0)
