def sample_inputs_narrow(op_info, device, dtype, requires_grad, **kwargs):
    shapes_and_args = (
        ((S, S, S), (1, 2, 2)),
        ((S, S, S), (-1, 2, 2)),
        ((S, S, S), (1, 0, 0)),
        ((S, S, S), (-1, 0, 0)),
    )

    for shape, args in shapes_and_args:
        tensor = make_tensor(shape, device, dtype, low=None, high=None,
                             requires_grad=requires_grad)
        yield SampleInput(tensor, args=args)
