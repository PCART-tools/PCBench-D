def sample_inputs_cross(op_info, device, dtype, requires_grad, **kwargs):
    sample0 = SampleInput(make_tensor((S, 3), device=device, dtype=dtype, requires_grad=requires_grad),
                          args=(make_tensor((S, 3), device=device, dtype=dtype, requires_grad=requires_grad),))
    sample1 = SampleInput(make_tensor((S, 3, S), device=device, dtype=dtype, requires_grad=requires_grad),
                          args=(make_tensor((S, 3, S), device=device, dtype=dtype, requires_grad=requires_grad),),
                          kwargs={'dim': 1})

    return (sample0, sample1)
