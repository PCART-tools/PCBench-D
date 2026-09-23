def sample_inputs_cholesky_solve(op_info, device, dtype, requires_grad=False, **kwargs):
    out = sample_inputs_linalg_cholesky_inverse(
        op_info, device, dtype, requires_grad=False
    )

    for sample in out:
        psd_matrix = sample.input
        sample.input = make_tensor(psd_matrix.shape, device, dtype, requires_grad=requires_grad, low=None, high=None)
        sample.args = (psd_matrix.requires_grad_(requires_grad),)

    return out
