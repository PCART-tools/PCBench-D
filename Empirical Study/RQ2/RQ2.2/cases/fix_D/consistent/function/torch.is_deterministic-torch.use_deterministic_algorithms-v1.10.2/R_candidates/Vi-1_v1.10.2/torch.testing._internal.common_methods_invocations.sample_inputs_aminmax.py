def sample_inputs_aminmax(op_info, device, dtype, requires_grad, **kwargs):
    test_cases: Tuple[tuple, dict] = (  # type: ignore[assignment]
        ((S, S, S), {}),
        ((S, S, S), {'dim': 1}),
        ((S, S, S), {'dim': 1, 'keepdim': True}),
        ((), {'dim': 0}),
        ((), {}),
        ((), {'dim': 0, 'keepdim': True}),
    )

    samples: List[SampleInput] = []
    for shape, kwargs in test_cases:
        samples.append(SampleInput(
            make_tensor(shape, device, dtype, requires_grad=requires_grad),
            kwargs=kwargs))

    return samples
