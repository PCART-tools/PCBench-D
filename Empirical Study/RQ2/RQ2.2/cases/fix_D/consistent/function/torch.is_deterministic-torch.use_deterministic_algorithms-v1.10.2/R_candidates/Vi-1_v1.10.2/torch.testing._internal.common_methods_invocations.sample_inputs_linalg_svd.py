def sample_inputs_linalg_svd(op_info, device, dtype, requires_grad=False, **kwargs):
    return _sample_inputs_svd(op_info, device, dtype, requires_grad, is_linalg_svd=True)
