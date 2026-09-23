def sample_inputs_linalg_cholesky_inverse(op_info, device, dtype, requires_grad=False, **kwargs):
    # Generate Cholesky factors of positive-definite (non-singular) Hermitian (symmetric) matrices
    from torch.testing._internal.common_utils import random_hermitian_pd_matrix
    inputs = (
        torch.zeros(0, 0, dtype=dtype, device=device),  # 0x0 matrix
        torch.zeros(0, 2, 2, dtype=dtype, device=device),  # zero batch of matrices
        random_hermitian_pd_matrix(S, dtype=dtype, device=device),  # single matrix
        random_hermitian_pd_matrix(S, 2, dtype=dtype, device=device),  # batch of matrices
    )
    test_cases = (torch.linalg.cholesky(a) for a in inputs)
    out = []
    for a in test_cases:
        a.requires_grad = requires_grad
        out.append(SampleInput(a))
        out.append(SampleInput(a.clone().requires_grad_(requires_grad), kwargs=dict(upper=True)))
    return out
