def _gradcheck_helper(func, inputs, eps, atol, rtol, check_sparse_nnz, nondet_tol, check_undefined_grad,
                      check_grad_dtypes, check_batched_grad, check_forward_ad, fast_mode):
    tupled_inputs = _as_tuple(inputs)
    _check_inputs(tupled_inputs, check_sparse_nnz)

    func_out = func(*tupled_inputs)
    outputs = _differentiable_outputs(func_out)
    _check_outputs(outputs)

    gradcheck_fn = _fast_gradcheck if fast_mode else _slow_gradcheck
    _gradcheck_real_imag(gradcheck_fn, func, func_out, tupled_inputs, outputs, eps,
                         rtol, atol, check_grad_dtypes, check_forward_ad=check_forward_ad, nondet_tol=nondet_tol)

    for i, o in enumerate(outputs):
        if check_batched_grad:
            _test_batched_grad(tupled_inputs, o, i)

    _test_backward_mul_by_grad_output(outputs, tupled_inputs, check_sparse_nnz)

    if check_undefined_grad:
        _test_undefined_grad(func, outputs, tupled_inputs)
    return True
