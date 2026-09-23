def sample_inputs_bmm(self, device, dtype, requires_grad, **kwargs):
    return (
        SampleInput(
            make_tensor((M, S, M, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                make_tensor((M, M, S, ), device, dtype, low=None, high=None, requires_grad=requires_grad),
            )
        ),
    )
