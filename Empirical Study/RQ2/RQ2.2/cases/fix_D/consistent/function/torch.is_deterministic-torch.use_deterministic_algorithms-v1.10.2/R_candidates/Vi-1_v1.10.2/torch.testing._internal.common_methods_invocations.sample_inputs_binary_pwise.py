def sample_inputs_binary_pwise(
    op_info,
    device,
    dtype,
    requires_grad,
    *,
    python_scalars=False,
    op_kwargs=None,
    lhs_make_tensor_kwargs=None,
    rhs_make_tensor_kwargs=None,
    **kwargs,
):
    op_kwargs, lhs_make_tensor_kwargs, rhs_make_tensor_kwargs = _resolve_binay_pwise_kwargs(
        op_info,
        op_kwargs=op_kwargs,
        lhs_make_tensor_kwargs=lhs_make_tensor_kwargs,
        rhs_make_tensor_kwargs=rhs_make_tensor_kwargs,
    )

    scalar = make_tensor((), device=device, dtype=dtype, **rhs_make_tensor_kwargs)
    if python_scalars:
        scalar = scalar.item()  # type: ignore[assignment]

    shapes = [
        ((), scalar),
        ((S,), scalar),
        ((S, 1), (S,)),
        ((M, S), scalar),
        ((S, M, S), (M, S)),
        ((S, M, S), (S, M, S)),
        ((M, 1, S), (M, S)),
        ((M, 1, S), (1, M, S)),
    ]

    sample_inputs = []
    for shape_lhs, shape_rhs_or_scalar in shapes:
        lhs = make_tensor(
            shape_lhs,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
            **lhs_make_tensor_kwargs,
        )
        if isinstance(shape_rhs_or_scalar, tuple):
            # shape
            rhs = make_tensor(
                shape_rhs_or_scalar,
                device=device,
                dtype=dtype,
                requires_grad=requires_grad,
                **rhs_make_tensor_kwargs,
            )
            broadcasts_input = torch.broadcast_shapes(shape_lhs, shape_rhs_or_scalar) != shape_lhs
        else:
            # scalar
            rhs = shape_rhs_or_scalar  # type: ignore[assignment]
            broadcasts_input = False

        sample_inputs.append(SampleInput(lhs, args=(rhs,), kwargs=op_kwargs, broadcasts_input=broadcasts_input))
    return sample_inputs
