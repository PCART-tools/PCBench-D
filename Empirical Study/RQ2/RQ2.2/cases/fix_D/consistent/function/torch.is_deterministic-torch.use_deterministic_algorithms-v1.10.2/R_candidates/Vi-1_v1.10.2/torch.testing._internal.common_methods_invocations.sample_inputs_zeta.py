def sample_inputs_zeta(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    samples = (SampleInput(make_arg((S,), low=1, requires_grad=requires_grad),
                           args=(make_arg((S,), low=2, requires_grad=False),)),
               SampleInput(make_arg((S,), low=1, requires_grad=requires_grad),
                           args=(3.,)),
               )

    return samples
