def sample_inputs_lu_solve(op_info, device, dtype, requires_grad=False, **kwargs):
    from torch.testing._internal.common_utils import random_fullrank_matrix_distinct_singular_value

    batches = [(), (0, ), (2, )]
    ns = [5, 3, 0]
    nrhs = [0, 1, 6]

    def generate_samples():
        for n, batch, rhs in product(ns, batches, nrhs):
            a = random_fullrank_matrix_distinct_singular_value(n, *batch, dtype=dtype, device=device)
            requires_grad_options = (False,) if not requires_grad else (True, False)
            # we try all possible combinations of requires_grad for each input
            for lu_requires_grad, b_requires_grad in product(requires_grad_options, requires_grad_options):
                # when requires_grad == True, at least one input has to have requires_grad enabled
                if requires_grad and not lu_requires_grad and not b_requires_grad:
                    continue
                # we run LU several times to guarantee that the produced SampleInputs are independent
                # this is especially important when setting different requries_grad for same tensors!
                lu, pivs = a.lu()
                lu.requires_grad = lu_requires_grad
                b = torch.randn(*batch, n, rhs, dtype=dtype, device=device)
                b.requires_grad = b_requires_grad
                yield SampleInput(b, args=(lu, pivs))

    return list(generate_samples())
