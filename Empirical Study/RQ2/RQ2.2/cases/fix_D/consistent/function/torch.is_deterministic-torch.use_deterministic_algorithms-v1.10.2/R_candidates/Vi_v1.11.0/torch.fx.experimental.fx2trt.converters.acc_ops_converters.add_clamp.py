def add_clamp(network, input, val, op):
    acc_ops_clamp_shape = (1,) * len(input.shape)  # broadcast all dimensions
    acc_ops_clamp_tensor = (
        val
        * torch.ones(acc_ops_clamp_shape, dtype=torch_dtype_from_trt(input.dtype))
        .cpu()
        .numpy()
    )
    acc_ops_clamp_trt = network.add_constant(acc_ops_clamp_shape, acc_ops_clamp_tensor)
    layer = network.add_elementwise(input, acc_ops_clamp_trt.get_output(0), op)

    return layer
