@tensorrt_converter(acc_ops.dequantize)
def acc_ops_dequantize(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"{name} received input {input_val} that is not part "
                           "of the TensorRT region!")

    q_scale = acc_utils.get_field_from_acc_out_ty(kwargs["input_tensor_meta"], "q_scale")
    q_zero_point = acc_utils.get_field_from_acc_out_ty(kwargs["input_tensor_meta"], "q_zero_point")
    dtype = acc_utils.get_field_from_acc_out_ty(kwargs["input_tensor_meta"], "dtype")

    if dtype not in (torch.quint8, torch.qint8, torch.qint32):
        raise RuntimeError("Only support (torch.quint8, torch.qint8, torch.qint32) "
                           f"quantized type in dequantize, get {dtype}.")

    if q_zero_point != 0:
        raise RuntimeError(f"Only support zero_point == 0, get {q_zero_point}")

    scale_layer = network.add_constant((1,), trt.Weights(np.ascontiguousarray([q_scale], dtype=np.float32)))
    scale_layer.name = input_val.name + ".dequant.scale"
    scale = scale_layer.get_output(0)
    # assert trt.__version__ > "8.0", "Explicit dequantize op is only supported in "
    # "TensorRT 8.0 or above, current TensorRT version:" + trt.__version__
    layer = network.add_dequantize(input=input_val, scale=scale)
    layer.name = input_val.name + ".dequant"
    layer.axis = 0
    return layer.get_output(0)
