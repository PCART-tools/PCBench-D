def _sample_inputs_svd(op_info, device, dtype, requires_grad=False, is_linalg_svd=False):
    """
    This function generates input for torch.svd with distinct singular values so that autograd is always stable.
    Matrices of different size:
        square matrix - S x S size
        tall marix - S x (S-2)
        wide matrix - (S-2) x S
    and batched variants of above are generated.
    Each SampleInput has a function 'output_process_fn_grad' attached to it that is applied on the output of torch.svd
    It is needed for autograd checks, because backward of svd doesn't work for an arbitrary loss function.
    """
    from torch.testing._internal.common_utils import random_fullrank_matrix_distinct_singular_value

    # svd and linalg.svd returns V and V.conj().T, respectively. So we need to slice
    # along different dimensions when needed (this is used by
    # test_cases2:wide_all and wide_all_batched below)
    if is_linalg_svd:
        def slice_V(v):
            return v[..., :(S - 2), :]

        def uv_loss(usv):
            u00 = usv[0][0, 0]
            v00_conj = usv[2][0, 0]
            return u00 * v00_conj
    else:
        def slice_V(v):
            return v[..., :, :(S - 2)]

        def uv_loss(usv):
            u00 = usv[0][0, 0]
            v00_conj = usv[2][0, 0].conj()
            return u00 * v00_conj

    test_cases1 = (  # some=True (default)
        # loss functions for complex-valued svd have to be "gauge invariant",
        # i.e. loss functions shouldn't change when sigh of the singular vectors change.
        # the simplest choice to satisfy this requirement is to apply 'abs'.
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device),
            lambda usv: usv[1]),  # 'check_grad_s'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device),
            lambda usv: abs(usv[0])),  # 'check_grad_u'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device),
            lambda usv: abs(usv[2])),  # 'check_grad_v'
        # this test is important as it checks the additional term that is non-zero only for complex-valued inputs
        # and when the loss function depends both on 'u' and 'v'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device),
            uv_loss),  # 'check_grad_uv'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device)[:(S - 2)],
            lambda usv: (abs(usv[0]), usv[1], abs(usv[2][..., :, :(S - 2)]))),  # 'wide'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device)[:, :(S - 2)],
            lambda usv: (abs(usv[0]), usv[1], abs(usv[2]))),  # 'tall'
        (random_fullrank_matrix_distinct_singular_value(S, 2, dtype=dtype).to(device),
            lambda usv: (abs(usv[0]), usv[1], abs(usv[2]))),  # 'batched'
        (random_fullrank_matrix_distinct_singular_value(S, 2, dtype=dtype).to(device)[..., :(S - 2), :],
            lambda usv: (abs(usv[0]), usv[1], abs(usv[2]))),  # 'wide_batched'
        (random_fullrank_matrix_distinct_singular_value(S, 2, dtype=dtype).to(device)[..., :, :(S - 2)],
            lambda usv: (abs(usv[0]), usv[1], abs(usv[2]))),  # 'tall_batched'
    )
    test_cases2 = (  # some=False
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device)[:(S - 2)],
            lambda usv: (abs(usv[0]), usv[1], abs(slice_V(usv[2])))),  # 'wide_all'
        (random_fullrank_matrix_distinct_singular_value(S, dtype=dtype).to(device)[:, :(S - 2)],
            lambda usv: (abs(usv[0][:, :(S - 2)]), usv[1], abs(usv[2]))),  # 'tall_all'
        (random_fullrank_matrix_distinct_singular_value(S, 2, dtype=dtype).to(device)[..., :(S - 2), :],
            lambda usv: (abs(usv[0]), usv[1], abs(slice_V(usv[2])))),  # 'wide_all_batched'
        (random_fullrank_matrix_distinct_singular_value(S, 2, dtype=dtype).to(device)[..., :, :(S - 2)],
            lambda usv: (abs(usv[0][..., :, :(S - 2)]), usv[1], abs(usv[2]))),  # 'tall_all_batched'
    )

    out = []
    for a, out_fn in test_cases1:
        a.requires_grad = requires_grad
        if is_linalg_svd:
            kwargs = {'full_matrices': False}
        else:
            kwargs = {'some': True}
        out.append(SampleInput(a, kwargs=kwargs, output_process_fn_grad=out_fn))

    for a, out_fn in test_cases2:
        a.requires_grad = requires_grad
        if is_linalg_svd:
            kwargs = {'full_matrices': True}
        else:
            kwargs = {'some': False}
        out.append(SampleInput(a, kwargs=kwargs, output_process_fn_grad=out_fn))

    return out
