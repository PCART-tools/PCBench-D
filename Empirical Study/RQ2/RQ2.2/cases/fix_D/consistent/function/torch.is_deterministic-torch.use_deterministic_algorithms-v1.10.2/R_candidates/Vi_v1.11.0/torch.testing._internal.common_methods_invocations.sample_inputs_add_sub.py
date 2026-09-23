def sample_inputs_add_sub(
    op_info,
    device,
    dtype,
    requires_grad,
    python_scalars=False,
    alpha=1,
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

    lhs = make_tensor((S, S), device=device, dtype=dtype, requires_grad=requires_grad, **lhs_make_tensor_kwargs)
    rhs = make_tensor((S, S), device=device, dtype=dtype, requires_grad=requires_grad, **rhs_make_tensor_kwargs)
    yield SampleInput(lhs, args=(rhs,), kwargs=dict(op_kwargs, alpha=alpha), broadcasts_input=False)
