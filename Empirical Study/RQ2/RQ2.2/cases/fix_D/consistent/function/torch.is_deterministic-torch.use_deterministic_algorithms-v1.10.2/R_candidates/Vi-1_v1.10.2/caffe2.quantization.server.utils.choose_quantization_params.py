def choose_quantization_params(tensor_min, tensor_max, preserve_sparsity=False):
    if tensor_min < 0 and tensor_max > 0 and preserve_sparsity:
        symmetric_qmin = -(255 // 2 + 1)
        symmetric_qmax = 255 // 2
        max_scale = max(
            abs(tensor_min / symmetric_qmin), abs(tensor_max / symmetric_qmax)
        )
        tensor_min = max_scale * symmetric_qmin
        tensor_max = max_scale * symmetric_qmax

    q_param = hardcode_scale_zp.choose_quantization_params(tensor_min, tensor_max)

    if tensor_min < 0 and tensor_max > 0 and preserve_sparsity:
        q_param = hardcode_scale_zp.QuantizationParam(q_param.scale, 128)

    return q_param
