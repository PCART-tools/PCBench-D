def sample_inputs_sort(op_info, device, dtype, requires_grad, **kwargs):
    def apply_grad(t):
        if dtype in floating_types_and(torch.float16, torch.bfloat16):
            t.requires_grad_(requires_grad)

    def small_3d_unique(dtype, device):
        res = torch.randperm(S * S * S, dtype=torch.int64, device=device).view(S, S, S)
        res = res.to(dtype)
        apply_grad(res)
        return res

    def large_1d_unique(dtype, device):
        res = torch.randperm(L * L * L, dtype=torch.int64, device=device)
        res = res.to(dtype)
        apply_grad(res)
        return res

    samples = []
    # Test case for large tensor.
    largesample = SampleInput(large_1d_unique(dtype, device))
    samples.append(largesample)

    # Test cases for small 3d tensors.
    # Imitates legacy tests from test/test_torch.py
    t = small_3d_unique(dtype, device)
    dims = range(-3, 3)
    flag = [True, False]
    for dim, descending, stable in product(dims, flag, flag):
        # default schema without stable sort
        samples.append(SampleInput(t, args=(dim, descending)))
        # schema with stable sort, no CUDA support yet
        if torch.device(device).type == 'cpu':
            samples.append(
                SampleInput(t, kwargs=dict(dim=dim, descending=descending, stable=stable))
            )

    # Test cases for scalar tensor
    scalar = torch.tensor(1, dtype=dtype, device=device)
    apply_grad(scalar)
    samples.append(SampleInput(scalar))
    samples.append(SampleInput(scalar, args=(0,)))
    samples.append(SampleInput(scalar, args=(0, True)))

    # Test cases for stable sort
    samples.append(SampleInput(scalar, kwargs=dict(stable=True)))
    samples.append(SampleInput(scalar, kwargs=dict(dim=0, stable=True)))
    samples.append(SampleInput(scalar, kwargs=dict(dim=0, descending=True, stable=True)))
    return samples
