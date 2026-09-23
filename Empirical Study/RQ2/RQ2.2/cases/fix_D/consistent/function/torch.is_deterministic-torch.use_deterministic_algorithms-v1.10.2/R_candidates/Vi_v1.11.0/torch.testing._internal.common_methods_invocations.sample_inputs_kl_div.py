def sample_inputs_kl_div(op_info, device, dtype, requires_grad, **kwargs):
    make = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes_and_reduction = [
        ((2,), "mean"),
        ((2, 3), "mean"),
        ((2, 3, 4), "mean"),
        ((2,), "none"),
        ((2,), "batchmean"),
        ((2,), "sum"),
    ]

    sample_inputs = []
    for (shape, reduction), log_target in itertools.product(shapes_and_reduction, (True, False)):
        # input should be log-probability, i.e. lie in (-inf, 0]
        input = make(shape, low=None, high=0)
        # target should be a probability by default, i.e. lie in [0, 1], and a log-probability if log_target is set,
        # i.e. lie in (-inf, 0]
        target = make(shape, low=None, high=0) if log_target else make(shape, low=0, high=1)
        sample_inputs.append(
            SampleInput(input, args=(target,), kwargs=dict(reduction=reduction, log_target=log_target))
        )
    return sample_inputs
