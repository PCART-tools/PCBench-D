def add_quantization_param_args(op, tensor, preserve_sparsity=False):
    tensor_min = 0 if tensor.size == 0 else tensor.min()
    tensor_max = 0 if tensor.size == 0 else tensor.max()

    q_param = choose_quantization_params(tensor_min, tensor_max, preserve_sparsity)

    add_quantization_param_args_(op, q_param)
    return q_param
