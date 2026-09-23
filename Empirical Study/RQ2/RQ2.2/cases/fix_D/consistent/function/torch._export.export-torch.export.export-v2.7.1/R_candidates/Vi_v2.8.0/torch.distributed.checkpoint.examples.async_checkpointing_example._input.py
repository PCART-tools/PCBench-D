def _input():
    x = torch.rand(128, 8, device="cuda")
    y = torch.zeros(128, 1, device="cuda")

    y[torch.sum(x, dim=1) >= 4] = 1.0

    return x, y
