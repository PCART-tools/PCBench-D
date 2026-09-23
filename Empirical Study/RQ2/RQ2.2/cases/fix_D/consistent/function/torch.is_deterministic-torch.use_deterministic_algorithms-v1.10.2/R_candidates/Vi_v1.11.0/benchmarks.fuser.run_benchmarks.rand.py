def rand(*shape):
    return torch.rand(*shape).mul(16).add(1)
