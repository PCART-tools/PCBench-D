def hardswish(x):
    return x * torch.clamp(x + 3.0, 0.0, 6.0) / 6.0
