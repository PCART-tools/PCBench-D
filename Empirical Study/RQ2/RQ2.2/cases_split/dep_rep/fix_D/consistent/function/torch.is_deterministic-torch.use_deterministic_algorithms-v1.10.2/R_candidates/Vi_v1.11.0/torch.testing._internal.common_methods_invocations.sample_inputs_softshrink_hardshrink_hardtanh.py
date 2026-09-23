def sample_inputs_softshrink_hardshrink_hardtanh(op_info, device, dtype, requires_grad=False, **kwargs):
    N = 10
    tensors = [SampleInput(make_tensor((N, N), device=device, dtype=dtype,
               requires_grad=requires_grad)) for _ in range(1, N)]
    return tensors
