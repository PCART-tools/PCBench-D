def sample_inputs_hardswish(self, device, dtype, requires_grad):
    N = 5
    # make sure we are testing -3 -> 3 range. default is -10 -> 10 so maybe unnecessary ?
    tensors = [SampleInput(make_tensor((N * 2, N * 2), device=device, dtype=dtype,
               requires_grad=requires_grad, low=-5, high=5)) for _ in range(1, N)]
    return tensors
