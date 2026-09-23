def sample_inputs_atleast1d2d3d(op_info, device, dtype, requires_grad, **kwargs):
    input_list = []
    shapes = ((S, S, S, S), (S, S, S), (S, S), (S, ), (),)
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    samples = []
    for shape in shapes:
        input_list.append(make_tensor_partial(shape))
        samples.append(SampleInput(make_tensor_partial(shape)))
    samples.append(SampleInput(input_list, ))
    return samples
