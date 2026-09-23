def sample_inputs_clamp(op_info, device, dtype, requires_grad, **kwargs):
    x = make_tensor((S, M, S), device, dtype, low=None, high=None, requires_grad=requires_grad)
    lb = make_tensor((S, M, S), device, dtype, low=None, high=None, requires_grad=requires_grad)
    ub = make_tensor((S, M, S), device, dtype, low=None, high=None, requires_grad=requires_grad)

    def detach(tensor):
        return tensor.clone().detach_().requires_grad_(requires_grad)

    return [
        SampleInput(detach(x), args=(lb, ub)),
        SampleInput(detach(x), args=(detach(lb[0]), detach(ub[0]))),
        SampleInput(detach(x), args=(detach(lb[:, :1]),)),
    ]
