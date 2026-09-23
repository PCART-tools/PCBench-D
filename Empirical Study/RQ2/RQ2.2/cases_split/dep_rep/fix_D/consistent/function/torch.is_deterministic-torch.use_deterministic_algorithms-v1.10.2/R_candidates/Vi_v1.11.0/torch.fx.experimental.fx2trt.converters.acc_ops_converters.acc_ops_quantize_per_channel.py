@tensorrt_converter(acc_ops.quantize_per_channel)
def acc_ops_quantize_per_channel(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = get_trt_tensor(network, kwargs["input"], f"{name}_input")

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"{name} received input {input_val} that is not part "
                           "of the TensorRT region!")

    qparams = TensorMetadata(*kwargs["acc_out_ty"]).qparams  # type: ignore[misc]
    q_per_channel_scales = qparams["scale"]
    q_per_channel_zero_points = qparams["zero_point"]
    q_per_channel_axis = qparams["axis"]
    dtype = TensorMetadata(*kwargs["acc_out_ty"]).dtype  # type: ignore[misc]
    if dtype not in (torch.quint8, torch.qint8, torch.qint32):
        raise RuntimeError("Only support (torch.quint8, torch.qint8, torch.qint32) "
                           f"quantized type in quantize_per_tensor, get {dtype}.")

    # Make sure zero_points are all 0 because only symmetric quantization
    # is supported in TensorRT
    if not torch.equal(
            q_per_channel_zero_points,
            torch.zeros(q_per_channel_zero_points.shape, dtype=q_per_channel_zero_points.dtype)):
        raise RuntimeError(f"Only support zero_point == 0, get {q_per_channel_zero_points}")

    if not torch.all(torch.ge(q_per_channel_scales, 0)):
        raise RuntimeError(f"All scale values must be >= 0, get {q_per_channel_scales}")

    scale_layer = network.add_constant(
        q_per_channel_scales.shape,
        trt.Weights(np.ascontiguousarray(q_per_channel_scales, dtype=np.float32)))
    scale_layer.name = input_val.name + ".per_channel_quant.scale"
    scale = scale_layer.get_output(0)
    # assert trt.__version__ > "8.0", "Explicit quantize op is only supported in "
    # "TensorRT 8.0 or above, current TensorRT version:" + trt.__version__
    layer = network.add_quantize(input=input_val, scale=scale)
    layer.axis = q_per_channel_axis
    set_layer_name(layer, target, f"{input_val.name}_per_channel_quant")
    return layer.get_output(0)
