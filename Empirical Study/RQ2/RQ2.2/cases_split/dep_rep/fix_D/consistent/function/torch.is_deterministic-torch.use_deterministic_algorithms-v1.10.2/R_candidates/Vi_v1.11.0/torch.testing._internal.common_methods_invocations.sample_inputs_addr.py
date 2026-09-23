def sample_inputs_addr(op_info, device, dtype, requires_grad, **kwargs):
    input1 = SampleInput(
        make_tensor((S, M), device, dtype, low=None, high=None, requires_grad=requires_grad),
        args=(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad)))

    input2 = SampleInput(
        make_tensor((), device, dtype, low=None, high=None, requires_grad=requires_grad),
        args=(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad)),
        broadcasts_input=True)

    if dtype.is_complex:
        alpha, beta = 0.1 + 0.3j, 0.4 + 0.6j
    elif dtype.is_floating_point:
        alpha, beta = 0.2, 0.6
    else:
        alpha, beta = 2, 3

    input3 = SampleInput(
        make_tensor((S, M), device, dtype, low=None, high=None, requires_grad=requires_grad),
        args=(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad)),
        kwargs=dict(beta=beta, alpha=alpha))

    input4 = SampleInput(
        make_tensor((), device, dtype, low=None, high=None, requires_grad=requires_grad),
        args=(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad)),
        kwargs=dict(beta=beta, alpha=alpha),
        broadcasts_input=True)

    return (input1, input2, input3, input4)
