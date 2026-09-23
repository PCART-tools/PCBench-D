def trivial_graph(a, b, c):
    s = torch.tensor([[3, 3], [3, 3]])
    return a + b * c + s
