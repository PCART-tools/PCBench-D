def gen_int_comparison_tensors(N, M):
    return (torch.randint(0, 3, (N, M)), torch.randint(0, 3, (N, M)), torch.empty((N, M), dtype=torch.bool))
