@tensorrt_converter(acc_ops.dequantize)
def acc_ops_dequantize(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    input_val_tensor_meta = kwargs["_itensor_to_tensor_meta"][input_val]  # type: ignore[index]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"{name} received input {input_val} that is not part "
                           "of the TensorRT region!")

    qparams = TensorMetadata(*input_val_tensor_meta).qparams  # type: ignore[misc]
    qscheme = qparams["qscheme"]
    if qscheme == torch.per_tensor_affine:
        q_scale = qparams["scale"]
        q_zero_point = qparams["zero_point"]
        q_axis = 0
        scale_shape = (1,)
        if q_zero_point != 0:
            raise RuntimeError(f"Only support zero_point == 0, get {q_zero_point}")
    elif qscheme == torch.per_channel_affine:
        q_scale = qparams["scale"]
        q_zero_point = qparams["zero_point"]
        q_axis = qparams["axis"]
        assert isinstance(q_scale, immutable_list), "expected q_scale to be immutable_list got {}".format(type(q_scale))
        scale_shape = (len(q_scale),)
        if any(x != 0 for x in q_zero_point):
            raise RuntimeError(f"Only support zero_point == 0, get {q_zero_point}")
    else:
        raise RuntimeError("Unsupported qscheme in dequantize: {qscheme}")

    dtype = TensorMetadata(*input_val_tensor_meta).dtype  # type: ignore[misc]

    if dtype not in (torch.quint8, torch.qint8, torch.qint32):
        raise RuntimeError("Only support (torch.quint8, torch.qint8, torch.qint32) "
                           f"quantized type in dequantize, get {dtype}.")

    scale_layer = network.add_constant(scale_shape, trt.Weights(np.ascontiguousarray(q_scale, dtype=np.float32)))
    scale_layer.name = input_val.name + ".dequant.scale"
    scale = scale_layer.get_output(0)
    # assert trt.__version__ > "8.0", "Explicit dequantize op is only supported in "
    # "TensorRT 8.0 or above, current TensorRT version:" + trt.__version__
    layer = network.add_dequantize(input=input_val, scale=scale)
    set_layer_name(layer, target, f"{input_val.name}_.dequant")
    layer.axis = q_axis
    return layer.get_output(0)
