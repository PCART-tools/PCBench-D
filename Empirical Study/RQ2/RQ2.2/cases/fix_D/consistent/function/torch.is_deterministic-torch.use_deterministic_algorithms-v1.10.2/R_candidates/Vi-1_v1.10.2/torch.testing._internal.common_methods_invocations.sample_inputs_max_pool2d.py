def sample_inputs_max_pool2d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    kerneli = [[3, 2], 3]
    stridei = [[2, 2]]
    Ni = [1, 4, None]
    Ci = [32]
    Hi = [8, 16]
    Wi = [8, 16]
    ceil_modei = [True, False]
    paddingi = [0, 1]
    dilationi = [1, (1, 2)]
    return_indicesi = [True, False]

    products = product(kerneli, stridei, Ni, Ci, Hi, Wi, ceil_modei, paddingi, dilationi, return_indicesi)

    def generator():
        for kernel, stride, N, C, H, W, ceil_mode, padding, dilation, return_indices in products:
            max_pool = torch.nn.MaxPool2d(kernel, stride, ceil_mode=ceil_mode, padding=padding,
                                          dilation=dilation, return_indices=return_indices)
            kwargs = {
                "kernel_size": max_pool.kernel_size,
                "stride": max_pool.stride,
                "padding": max_pool.padding,
                "dilation": max_pool.dilation,
                "ceil_mode": max_pool.ceil_mode,
                "return_indices": max_pool.return_indices,
            }
            sample_input = make_arg((N, C, H, W)) if N is not None else (make_arg((C, H, W)))

            yield SampleInput(sample_input, kwargs=kwargs)

    return list(generator())
