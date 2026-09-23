def sample_inputs_linalg_pinv_hermitian(op_info, device, dtype, requires_grad=False, **kwargs):
    """
    This function generates input for torch.linalg.pinv with hermitian=True keyword argument.
    """
    out = sample_inputs_linalg_invertible(op_info, device, dtype, requires_grad, **kwargs)
    for o in out:
        o.kwargs = {"hermitian": True}
    return out
