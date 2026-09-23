def sample_inputs_xlogy(self, device, dtype, requires_grad, **kwargs):
    return (
        SampleInput(
            make_tensor((S, S), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                make_tensor((S, S), device, dtype, low=0, high=None, requires_grad=requires_grad),
            )
        ),
    )
