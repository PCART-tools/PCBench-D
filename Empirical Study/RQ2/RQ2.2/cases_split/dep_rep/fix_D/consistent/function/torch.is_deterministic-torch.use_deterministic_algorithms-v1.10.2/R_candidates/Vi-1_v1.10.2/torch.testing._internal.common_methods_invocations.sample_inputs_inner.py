def sample_inputs_inner(self, device, dtype, requires_grad, **kwargs):
    return (
        SampleInput(
            make_tensor((S, ), device, dtype, requires_grad=requires_grad),
            args=(
                make_tensor((S, ), device, dtype, requires_grad=requires_grad),
            )
        ),
        SampleInput(
            make_tensor((), device, dtype, requires_grad=requires_grad),
            args=(
                make_tensor((S, S), device, dtype, requires_grad=requires_grad),
            )
        ),
    )
