def sample_unsqueeze(op_info, device, dtype, requires_grad, **kwargs):
    shapes_and_axes = [
        ((3, 4, 5), 0),
        ((3, 4, 5), 1),
        ((3, 4, 5), 3),
        ((3, 4, 5), -1),
        ((3, 4, 5), -3),
        ((), 0)
    ]

    samples = []
    for shape, axis in shapes_and_axes:
        tensor = make_tensor(shape, device, dtype, low=None, high=None,
                             requires_grad=requires_grad)
        samples.append(SampleInput(tensor, args=(axis,),))

    return samples
