def _interpolate_size_to_scales(g, input, output_size, dim):
    output_size = _maybe_get_const(output_size, "is")
    if _is_value(output_size):
        offset = 2
        offsets = g.op("Constant", value_t=torch.ones(offset, dtype=torch.float32))
        dividend = g.op("Cast", output_size, to_i=cast_pytorch_to_onnx["Float"])
        divisor = _slice_helper(g, g.op("Shape", input), axes=[0], ends=[maxsize], starts=[offset])
        divisor = g.op("Cast", divisor, to_i=cast_pytorch_to_onnx["Float"])
        scale_dims = g.op("Div", dividend, divisor)
        scales = g.op("Concat", offsets, scale_dims, axis_i=0)
    else:
        scales_constant = [1. if i < 2 else
                           float(output_size[-(dim - i)]) / float(input.type().sizes()[-(dim - i)])
                           for i in range(0, dim)]
        scales = g.op("Constant", value_t=torch.tensor(scales_constant, dtype=torch.float32))
    return scales
