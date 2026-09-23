def gen_float_comparison_tensors(N, M):
    return (torch.rand(N, M), torch.rand(N, M), torch.empty((N, M), dtype=torch.bool))
