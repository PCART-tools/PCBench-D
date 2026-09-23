def sample_inputs_to(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    # test_multiple_devices_to_cuda would fail if we use a different device than given
    devices = [device]
    if torch.device(device).type == 'cpu':
        devices = [torch.device('cpu'), torch.device('cuda:0')] if torch.cuda.is_available() else devices
    memory_formats = [torch.preserve_format, torch.channels_last]

    # TODO: can't switch `to.device` overload to use positional arguments
    # https://github.com/pytorch/pytorch/issues/84265
    # to.device overload
    for device, nb, cp, mem_f in product(devices, [True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        yield SampleInput(make_arg((S, S, S, S)), args=(device, torch.float64, nb, cp), kwargs=kwargs)

    # to.dtype overload
    for nb, cp, mem_f in product([True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        yield SampleInput(make_arg((S, S, S, S)), args=(torch.float64, nb, cp), kwargs=kwargs)

    # to.other overload
    for device, nb, cp, mem_f in product(devices, [True, False], [True, False], memory_formats):
        kwargs = {
            "memory_format": mem_f,
        }
        other = make_arg((S, S, S, S), dtype=torch.float64, device=device)
        yield SampleInput(make_arg((S, S, S, S)), args=(other, nb, cp), kwargs=kwargs)
