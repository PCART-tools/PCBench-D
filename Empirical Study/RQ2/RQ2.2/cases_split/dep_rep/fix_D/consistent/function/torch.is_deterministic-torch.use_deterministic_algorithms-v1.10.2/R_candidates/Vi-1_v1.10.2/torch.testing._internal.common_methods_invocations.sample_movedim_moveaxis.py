def sample_movedim_moveaxis(op_info, device, dtype, requires_grad):
    return (
        SampleInput(
            make_tensor((4, 3, 2, 1), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=([0, 1, 2, 3], [3, 2, 1, 0])),
        SampleInput(
            make_tensor((4, 3, 2, 1), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=([0, -1, -2, -3], [-3, -2, -1, -0]))
    )
