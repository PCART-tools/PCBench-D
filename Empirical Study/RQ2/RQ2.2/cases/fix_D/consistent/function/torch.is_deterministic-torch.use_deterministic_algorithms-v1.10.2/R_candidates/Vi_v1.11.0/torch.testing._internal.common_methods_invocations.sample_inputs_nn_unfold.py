def sample_inputs_nn_unfold(op_info, device, dtype, requires_grad, **kwargs):
    shapes = ((0, 1, 5, 5), (1, 1, 5, 5), (2, 3, 5, 5))
    kernel_sizes = (2, (2, 2), (3, 3))
    dilations = (1, 2, (1, 2))
    paddings = (0, 1, (1, 1))
    strides = (1, 2, (1, 2))

    cases = product(shapes, kernel_sizes, dilations, paddings, strides)
    for shape, kernel_size, dilation, padding, stride in cases:
        tensor = make_tensor(shape, device, dtype, requires_grad=requires_grad)
        yield SampleInput(tensor, args=(kernel_size, dilation, padding, stride))

    # With default args
    yield SampleInput(make_tensor((1, 1, 5, 5), device, dtype, requires_grad=requires_grad),
                      args=((3, 3),))
