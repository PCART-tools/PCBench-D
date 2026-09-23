def sample_inputs_lu_solve(op_info, device, dtype, requires_grad=False, **kwargs):
    make_fn = make_fullrank_matrices_with_distinct_singular_values
    make_a = partial(make_fn, dtype=dtype, device=device)
    make_b = partial(make_tensor, dtype=dtype, device=device)

    batches = ((), (0, ), (2, ))
    ns = (5, 3, 0)
    nrhs = (0, 1, 6)

    for n, batch, rhs in product(ns, batches, nrhs):
        shape_a = batch + (n, n)
        a = make_a(*shape_a)
        lu, pivs = a.lu()
        lu = lu.contiguous()

        shape_b = batch + (n, rhs)
        b = make_b(shape_b)

        grads = (False,) if not requires_grad else (True, False)
        # we try all possible combinations of requires_grad for each input
        for lu_grad, b_grad in product(grads, grads):
            # when requires_grad == True, at least one input has to have requires_grad enabled
            if requires_grad and not lu_grad and not b_grad:
                continue

            lu_ = lu.clone()
            lu_.requires_grad_(lu_grad)
            b_ = b.clone()
            b_.requires_grad_(b_grad)
            yield SampleInput(b_, args=(lu_, pivs))
