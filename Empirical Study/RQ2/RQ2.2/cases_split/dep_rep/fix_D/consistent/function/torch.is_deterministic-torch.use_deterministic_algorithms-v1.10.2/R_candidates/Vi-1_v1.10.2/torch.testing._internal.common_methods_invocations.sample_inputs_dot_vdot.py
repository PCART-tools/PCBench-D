def sample_inputs_dot_vdot(self, device, dtype, requires_grad, **kwargs):
    sample_inputs = []
    sample_inputs.append(SampleInput(
        make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
        args=(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
        )
    ))
    if dtype.is_complex:
        # dot/vdot for (conj(input), conj(arg_tensor)) and (conj(input), arg_tensor)
        # is tested in test_conj_view (which tests operations with only conjugated input tensor
        # -- not conjugated arg tensors)
        sample_inputs.append(SampleInput(
            make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                torch.conj(make_tensor((S, ), device, dtype, low=None, high=None, requires_grad=requires_grad)),
            )
        ))
    return sample_inputs
