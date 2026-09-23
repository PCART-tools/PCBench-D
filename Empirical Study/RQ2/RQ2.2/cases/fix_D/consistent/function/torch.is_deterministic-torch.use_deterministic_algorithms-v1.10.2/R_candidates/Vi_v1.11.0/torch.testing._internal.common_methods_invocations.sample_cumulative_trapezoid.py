def sample_cumulative_trapezoid(op_info, device, dtype, requires_grad, **kwargs):

    y_shape_x_shape_and_kwargs = [
        ((2, 3), (2, 3), {}),
        ((2, 3), (2, 3), {'dim': 1}),
        ((6,), (6,), {}),
        ((6,), None, {}),
        # When 'cumulative_trapezoid' is called with an empty input, it does not produce an output with requires_grad
        # See Issue #{61619}
        # ((6,0), (6,0), {}),
        ((2, 3), (1, 3), {}),
        ((3, 3), (3, 3), {}),
        ((3, 3), (3, 3), {'dim': -2}),
        ((5,), None, {'dx': 2.0}),
        ((2, 2), None, {'dx': 3.0})
    ]
    samples = []
    for y_shape, x_shape, kwarg in y_shape_x_shape_and_kwargs:
        y_tensor = make_tensor(y_shape, device, dtype, low=None, high=None,
                               requires_grad=requires_grad)
        if x_shape is not None:
            x_tensor = make_tensor(x_shape, device, dtype, low=None, high=None,
                                   requires_grad=requires_grad)
            samples.append(SampleInput(y_tensor, args=(x_tensor,), kwargs=kwarg))
        else:
            samples.append(SampleInput(y_tensor, kwargs=kwarg))
    return samples
