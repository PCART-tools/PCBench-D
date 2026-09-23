@parse_args("v", "t", "i", "i", "i")
def fake_quantize_per_tensor_affine(g, inputs, scale, zero_point, quant_min=-128, quant_max=127):
    if quant_min not in [0, -128] or quant_max not in [127, 255]:
        raise RuntimeError(
            "ONNX defines [0, 255] for quint8 and [-128, 127] for qint8, got [{}, {}]".format(quant_min, quant_max))
    scale = scale.float().data  # Avoid exporter generating double type
    zero_point_dtype = torch.int8 if quant_min == -128 else torch.uint8
    zero_point = torch.tensor(zero_point, dtype=zero_point_dtype)  # ONNX requires zero_point to be tensor
    return g.op("DequantizeLinear", g.op("QuantizeLinear", inputs, scale, zero_point), scale, zero_point)
