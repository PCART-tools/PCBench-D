def sample_inputs_ormqr(op_info, device, dtype, requires_grad, **kwargs):
    # create a helper function wrapping `make_tensor`
    make_input = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    def gen_inputs():
        batches = [(), (0, ), (2, ), (2, 1)]
        ns = [5, 2, 0]
        tf = [True, False]
        for batch, (m, n), left, transpose in product(batches, product(ns, ns), tf, tf):
            reflectors = make_input((*batch, m, n))
            tau = make_input((*batch, min(m, n)))
            other_matrix_shape = (m, n) if left else (n, m)
            other = make_input((*batch, *other_matrix_shape))
            kwargs = {"left": left, "transpose": transpose}
            yield SampleInput(reflectors, args=(tau, other,), kwargs=kwargs)

    return tuple(gen_inputs())
