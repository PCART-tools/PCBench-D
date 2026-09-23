def create_int8_bias_tensor_fill(tensor, out_blob_name, x_q_param, w_q_param):
    """
    Similar to create_int8_given_tensor_fill, but for bias blobs to be stored
    as int32.
    """
    scale = x_q_param.scale * w_q_param.scale
    quantized_tensor = np.around(tensor / scale).astype(np.int32)
    quantized_tensor.reshape(-1)
    op = core.CreateOperator("Int8GivenIntTensorFill", [], out_blob_name)
    op.arg.extend(
        [
            utils.MakeArgument("values", quantized_tensor),
            utils.MakeArgument("shape", quantized_tensor.shape),
        ]
    )
    q_param = hardcode_scale_zp.QuantizationParam(scale, 0)
    add_quantization_param_args_(op, q_param)
    return op
