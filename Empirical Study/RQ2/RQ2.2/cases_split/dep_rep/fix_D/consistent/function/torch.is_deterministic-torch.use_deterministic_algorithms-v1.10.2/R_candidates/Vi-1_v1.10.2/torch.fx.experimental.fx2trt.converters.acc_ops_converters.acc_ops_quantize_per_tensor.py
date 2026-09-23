@tensorrt_converter(acc_ops.quantize_per_tensor)
def acc_ops_quantize_per_tensor(network, target, args, kwargs, name):
    input_val = get_trt_tensor(network, kwargs["input"], f"{name}_input")


    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"{name} received input {input_val} that is not part "
                           "of the TensorRT region!")

    q_scale = acc_utils.get_field_from_acc_out_ty(kwargs["acc_out_ty"], "q_scale")
    q_zero_point = acc_utils.get_field_from_acc_out_ty(kwargs["acc_out_ty"], "q_zero_point")
    dtype = acc_utils.get_field_from_acc_out_ty(kwargs["acc_out_ty"], "dtype")
    if dtype not in (torch.quint8, torch.qint8, torch.qint32):
        raise RuntimeError("Only support (torch.quint8, torch.qint8, torch.qint32) "
                           f"quantized type in quantize_per_tensor, get {dtype}.")

    if q_zero_point != 0:
        raise RuntimeError(f"Only support zero_point == 0, get {q_zero_point}")

    scale_layer = network.add_constant((1,), trt.Weights(np.ascontiguousarray([float(q_scale)], dtype=np.float32)))
    scale_layer.name = input_val.name + ".quant.scale"
    scale = scale_layer.get_output(0)
    # assert trt.__version__ > "8.0", "Explicit quantize op is only supported in "
    # "TensorRT 8.0 or above, current TensorRT version:" + trt.__version__
    layer = network.add_quantize(input=input_val, scale=scale)
    layer.axis = 0
    layer.name = input_val.name + ".quant"
    return layer.get_output(0)
