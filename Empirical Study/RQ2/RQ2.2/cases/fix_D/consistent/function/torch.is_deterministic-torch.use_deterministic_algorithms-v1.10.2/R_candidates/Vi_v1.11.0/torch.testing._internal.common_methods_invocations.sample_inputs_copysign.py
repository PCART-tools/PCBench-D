def sample_inputs_copysign(op_info, device, dtype, requires_grad, **kwargs):
    def _make_tensor(*shape, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    cases = [
        # no broadcast
        ((S, S, S), (S, S, S), False),
        # broadcast rhs
        ((S, S, S), (S, S), False),

        # scalar
        ((S, S), 3.14, False),
        # scalar positive zero
        ((S, S), 0.0, False),
        # scalar negative zero
        ((S, S), -0.0, False),
    ]

    # broadcast lhs
    cases.append(((S, S), (S, S, S), True))
    # broadcast all
    cases.append(((S, 1, S), (M, S), True))

    for input_shape, arg_val, broadcasts_input in cases:
        if isinstance(arg_val, tuple):
            arg = _make_tensor(*arg_val)
        else:
            # arg_val is scalar
            arg = arg_val

        yield SampleInput(_make_tensor(*input_shape), args=(arg, ), broadcasts_input=broadcasts_input)
