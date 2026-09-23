def sample_inputs_isclose(
    op_info,
    device,
    dtype,
    requires_grad,
    python_scalars=False,
    op_kwargs=None,
    lhs_make_tensor_kwargs=None,
    rhs_make_tensor_kwargs=None,
    **kwargs,
):
    op_kwargs, lhs_make_tensor_kwargs, rhs_make_tensor_kwargs = _resolve_binary_pwise_kwargs(
        op_info,
        op_kwargs=op_kwargs,
        lhs_make_tensor_kwargs=lhs_make_tensor_kwargs,
        rhs_make_tensor_kwargs=rhs_make_tensor_kwargs,
    )

    yield from sample_inputs_binary_pwise(
        op_info,
        device,
        dtype,
        requires_grad,
        python_scalars=python_scalars,
        op_kwargs=op_kwargs,
        lhs_make_tensor_kwargs=lhs_make_tensor_kwargs,
        rhs_make_tensor_kwargs=rhs_make_tensor_kwargs,
        **kwargs,
    )

    rtols = [0., 1e-7]
    atols = [0., 1e-7]
    equal_nans = [False, True]

    products = product(rtols, atols, equal_nans)

    for rtol, atol, equal_nan in products:
        lhs = make_tensor((S, S), device=device, dtype=dtype, requires_grad=requires_grad, **lhs_make_tensor_kwargs)
        rhs = make_tensor((S, S), device=device, dtype=dtype, requires_grad=requires_grad, **rhs_make_tensor_kwargs)

        yield SampleInput(lhs, args=(rhs,),
                          kwargs=dict(op_kwargs, rtol=rtol, atol=atol, equal_nan=equal_nan))
