def output_graph(a, b, c, iters: int):
    s = torch.tensor([[3, 3], [3, 3]])
    k = a + b * c + s
    d: Dict[int, torch.Tensor] = {}
    for i in range(iters):
        d[i] = k + i
    return d
