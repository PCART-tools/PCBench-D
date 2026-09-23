def sample_inputs_sort(op_info, device, dtype, requires_grad, **kwargs):
    def small_3d_unique():
        res = torch.randperm(S * S * S, dtype=torch.int64, device=device).view(S, S, S)
        res = res.to(dtype).requires_grad_(requires_grad)
        return res

    def large_1d_unique():
        res = torch.randperm(L * L * L, dtype=torch.int64, device=device)
        res = res.to(dtype).requires_grad_(requires_grad)
        return res

    samples = []
    # Test case for large tensor.
    samples.append(SampleInput(large_1d_unique()))

    # Test cases for small 3d tensors.
    # Imitates legacy tests from test/test_torch.py
    dims = range(-3, 3)
    flag = [True, False]
    for dim, descending, stable in product(dims, flag, flag):
        # default schema without stable sort
        samples.append(SampleInput(small_3d_unique(),
                                   args=(dim, descending)))
        # schema with stable sort, no CUDA support yet
        if torch.device(device).type == 'cpu':
            samples.append(
                SampleInput(small_3d_unique(),
                            kwargs=dict(dim=dim, descending=descending, stable=stable))
            )

    # Test cases for scalar tensor
    samples.append(SampleInput(torch.tensor(1, dtype=dtype, device=device, requires_grad=requires_grad)))
    samples.append(SampleInput(torch.tensor(1, dtype=dtype, device=device, requires_grad=requires_grad),
                               args=(0,)))
    samples.append(SampleInput(torch.tensor(1, dtype=dtype, device=device, requires_grad=requires_grad),
                               args=(0, True)))

    # Test cases for stable sort
    samples.append(SampleInput(small_3d_unique(),
                   kwargs=dict(stable=True)))
    samples.append(SampleInput(small_3d_unique(),
                   kwargs=dict(dim=0, stable=True)))
    samples.append(SampleInput(small_3d_unique(),
                   kwargs=dict(dim=0, descending=True, stable=True)))
    return samples
