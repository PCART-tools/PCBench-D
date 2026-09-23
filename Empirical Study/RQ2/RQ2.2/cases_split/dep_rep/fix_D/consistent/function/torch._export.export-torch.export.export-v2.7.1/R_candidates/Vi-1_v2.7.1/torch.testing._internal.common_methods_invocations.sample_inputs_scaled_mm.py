def sample_inputs_scaled_mm(op_info, device, dtype, requires_grad, **kwargs):
    make_mat_e4m3 = partial(make_tensor, device=device, dtype=torch.float8_e4m3fn, requires_grad=requires_grad)
    make_mat_e5m2 = partial(make_tensor, device=device, dtype=torch.float8_e5m2, requires_grad=requires_grad)
    make_scale = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)
    M, N, K = 15, 32, 16
    samples = []
    # two e4m3
    mat1 = make_mat_e4m3((M, K))
    mat2 = make_mat_e4m3((K, N)).t().contiguous().t()
    scale1 = make_scale((1,))
    scale2 = make_scale((1,))
    samples.append(SampleInput(mat1, mat2, scale1, scale2))
    # mat1 e4m3 mat2 e5m2
    mat1 = make_mat_e4m3((M, K))
    mat2 = make_mat_e5m2((K, N)).t().contiguous().t()
    scale1 = make_scale((1,))
    scale2 = make_scale((1,))
    samples.append(SampleInput(mat1, mat2, scale1, scale2))
    # mat1 e5m2 mat2 e4m3
    mat1 = make_mat_e5m2((M, K))
    mat2 = make_mat_e4m3((K, N)).t().contiguous().t()
    scale1 = make_scale((1,))
    scale2 = make_scale((1,))
    samples.append(SampleInput(mat1, mat2, scale1, scale2))

    yield from samples
