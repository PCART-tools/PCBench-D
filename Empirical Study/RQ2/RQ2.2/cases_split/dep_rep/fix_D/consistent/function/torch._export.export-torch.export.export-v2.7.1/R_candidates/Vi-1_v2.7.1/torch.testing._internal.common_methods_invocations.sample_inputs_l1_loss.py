def sample_inputs_l1_loss(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_loss(op_info, device, dtype, requires_grad, **kwargs)

    # test COMPLEX_TO_FLOAT promotion
    if dtype.is_complex:
        make = partial(make_tensor, (), device=device, requires_grad=requires_grad)
        yield SampleInput(make(dtype=dtype), args=(make(dtype=torch.double),))
        yield SampleInput(make(dtype=torch.double), args=(make(dtype=dtype),))
