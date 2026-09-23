def sample_inputs_linalg_det(op_info, device, dtype, requires_grad, **kwargs):
    kw = dict(device=device, dtype=dtype)
    inputs = [
        make_tensor((S, S), **kw),
        make_tensor((1, 1), **kw),  # 1x1
        random_symmetric_matrix(S, **kw),  # symmetric
        random_symmetric_psd_matrix(S, **kw),  # symmetric_psd
        random_symmetric_pd_matrix(S, **kw),  # symmetric_pd

        random_square_matrix_of_rank(S, S - 2, **kw),  # dim2_null
        random_square_matrix_of_rank(S, 1, **kw),  # rank1
        random_square_matrix_of_rank(S, 2, **kw),  # rank2

        make_fullrank_matrices_with_distinct_singular_values(S, S, **kw),  # full rank
        make_tensor((3, 3, S, S), **kw),  # batched
        make_tensor((3, 3, 1, 1), **kw),  # batched_1x1
        random_symmetric_matrix(S, 3, **kw),  # batched_symmetric
        random_symmetric_psd_matrix(S, 3, **kw),  # batched_symmetric_psd
        random_symmetric_pd_matrix(S, 3, **kw),  # batched_symmetric_pd
        make_fullrank_matrices_with_distinct_singular_values(S, 3, 3, **kw),  # batched fullrank
        make_tensor((0, 0), **kw),
        make_tensor((0, S, S), **kw),
    ]
    for t in inputs:
        t.requires_grad = requires_grad
    return [SampleInput(t) for t in inputs]
