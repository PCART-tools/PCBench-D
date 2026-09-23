@parse_args("v", "v", "v", "i")
def conv_tbc(g, input, weight, bias, pad):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, weight, bias, operator_s="conv_tbc", pad_i=pad)
    else:
        # input must have 3 dimensions, see:
        # https://github.com/pytorch/pytorch/blob/master/aten/src/ATen/native/ConvolutionTBC.cpp#L8-L10
        # input = (time, batch, in_channels)
        # weight = (kernel_width, in_channels, out_channels)
        # bias = (out_channels,)
        input = g.op("Transpose", input, perm_i=[1, 2, 0])
        weight = g.op("Transpose", weight, perm_i=[2, 1, 0])
        conv = conv1d(g, input, weight, bias, [1], [pad], [1], 1)
        return g.op("Transpose", conv, perm_i=[2, 0, 1])
