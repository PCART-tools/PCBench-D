def sample_inputs_nll_loss(op_info, device, dtype, requires_grad, **kwargs):
    batch_size, num_classes = shape = (2, 3)

    input_shape_and_kwargs: List[Tuple[Tuple[int, ...], Dict[str, Any]]] = [
        ((*shape, 1), dict()),
        ((*shape, 1, 2), dict()),
        ((*shape, 1, 2, 3), dict()),
        (shape, dict(weight=make_tensor((num_classes,), device=device, dtype=dtype).abs())),
        (shape, dict(ignore_index=num_classes // 2)),
        (shape, dict(reduction="sum")),
        (shape, dict(reduction="mean")),
    ]

    sample_inputs = []
    for input_shape, kwargs in input_shape_and_kwargs:
        input = make_tensor(input_shape, device=device, dtype=dtype, requires_grad=requires_grad)

        target = make_tensor(
            (batch_size, *input_shape[2:]),
            low=0,
            high=num_classes,
            device=device,
            dtype=torch.long,
            requires_grad=requires_grad
        )

        sample_inputs.append(SampleInput(input, args=(target,), kwargs=kwargs))

    return sample_inputs
