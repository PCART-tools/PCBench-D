def sample_inputs_lerp(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    samples = (
        # no broadcast
        SampleInput(make_arg((S, S)), args=(make_arg((S, S)), 0.4)),
        # broadcast rhs
        SampleInput(make_arg((S, S)), args=(make_arg((S,)), 0.4)),
        # scalar tensor
        SampleInput(make_arg(()), args=(make_arg(()), 0.4)),
        # broadcast rhs scalar-tensor
        SampleInput(make_arg((S, S)), args=(make_arg(()), 0.4)),
        # broadcast rhs with weight tensor
        SampleInput(make_arg((S, S)), args=(make_arg((S,)), make_arg((S, S)))),
        # broadcast rhs and weight tensor
        SampleInput(make_arg((S, S)), args=(make_arg((S, 1)), make_arg((S,)))),
        # broadcast lhs
        SampleInput(make_arg((S,)), args=(make_arg((S, S)), 0.4), broadcasts_input=True),
        # scalar broadcast_lhs
        SampleInput(make_arg(()), args=(make_arg((S, S)), 0.4), broadcasts_input=True),
        # broadcast all
        SampleInput(make_arg((S, 1)), args=(make_arg((S, S)), 0.4), broadcasts_input=True),
        # tensor broadcast all
        SampleInput(make_arg((S, 1)), args=(make_arg((S, S)), make_arg((S, 1))),
                    broadcasts_input=True),
        # no broadcast with weight tensor
        SampleInput(make_arg((S, S)), args=(make_arg((S, S)), make_arg((S, S)))),
        # broadcast lhs with weight tensor
        SampleInput(make_arg((S,)), args=(make_arg((S, S)), make_arg((S, S))), broadcasts_input=True),
        # broadcast lhs and weight tensor
        SampleInput(make_arg((S,)), args=(make_arg((S, S, S)), make_arg((S, S))), broadcasts_input=True),
        # broadcast lhs and weight tensor variant
        SampleInput(make_arg((S, S)), args=(make_arg((S, S, S)), make_arg((S,))), broadcasts_input=True),
    )

    if dtype.is_complex:
        samples = samples + (  # type: ignore[assignment]
            # no broadcast
            SampleInput(make_arg((S, S)), args=(make_arg((S, S)), 0.4j)),
            SampleInput(make_arg((S, S)), args=(make_arg((S, S)), 1.2 + 0.1j)),
            # broadcast rhs
            SampleInput(make_arg((S, S)), args=(make_arg((S,)), 0.4j)),
            SampleInput(make_arg((S, S)), args=(make_arg((S, S)), 5.4 + 9j)),
            # scalar tensor
            SampleInput(make_arg(()), args=(make_arg(()), 0.4j)),
            SampleInput(make_arg(()), args=(make_arg(()), 6.1 + 0.004j)),
            # broadcast rhs scalar-tensor
            SampleInput(make_arg((S, S)), args=(make_arg(()), 0.4j)),
            SampleInput(make_arg((S, S)), args=(make_arg(()), 1 + 2j)),
        )

    return samples
