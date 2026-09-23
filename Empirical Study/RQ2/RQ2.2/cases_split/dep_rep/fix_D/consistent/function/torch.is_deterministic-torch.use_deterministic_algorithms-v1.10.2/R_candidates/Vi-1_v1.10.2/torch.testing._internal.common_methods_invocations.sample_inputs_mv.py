def sample_inputs_mv(self, device, dtype, requires_grad, **kwargs):
    return (
        SampleInput(
            make_tensor((S, M, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            )
        ),
    )
