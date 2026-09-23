def sample_inputs_fmod_remainder(op_info, device, dtype, requires_grad, *, autodiffed=False, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    if autodiffed:
        samples = (
            ((S, S, S), 1.5, False),
            ((), 1.5, False),
        )
    else:
        cases = (
            ((S, S, S), (), False),
            ((S, S, S), (S, S, S), False),
            ((S, S, S), (S,), False),
        )

        # Sample inputs with scalars as torch tensors
        cases_with_tensor_scalar = (
            ((), torch.tensor(1, dtype=dtype, device=device, requires_grad=False), False),
        )

        # Sample inputs with broadcasting
        cases_with_broadcasting = (
            ((S,), (S, S, S), True),
            ((S, 1, S), (S, S, S), True),
            ((), (S, S, S), True),
        )

        samples = cases + cases_with_tensor_scalar + cases_with_broadcasting  # type: ignore[assignment]

    def generator():
        for shape, arg_other, broadcasts_input in samples:
            if isinstance(arg_other, tuple):
                arg = make_arg(arg_other, requires_grad=False, exclude_zero=True)
            else:
                # shape_other is scalar or torch.tensor
                arg = arg_other
            yield(SampleInput(make_arg(shape), args=(arg,), broadcasts_input=broadcasts_input))

    return list(generator())
