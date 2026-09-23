def create_int8_given_tensor_fill(tensor, out_blob_name, preserve_sparsity=False):
    """
    Create Int8GivenTensorFill op that quantizes the given tensor and outputs
    an Int8Tensor with out_blob_name.
    """
    op = core.CreateOperator("Int8GivenTensorFill", [], out_blob_name)
    q_param = add_quantization_param_args(op, tensor, preserve_sparsity)
    quantized_tensor = (
        np.around(tensor / q_param.scale).astype(np.int32) + q_param.zero_point
    )
    quantized_tensor = np.maximum(0, np.minimum(quantized_tensor, 255))
    op.arg.extend(
        [
            utils.MakeArgument("values", quantized_tensor.astype(np.uint8).tobytes()),
            utils.MakeArgument("shape", quantized_tensor.shape),
        ]
    )
    return op, q_param
