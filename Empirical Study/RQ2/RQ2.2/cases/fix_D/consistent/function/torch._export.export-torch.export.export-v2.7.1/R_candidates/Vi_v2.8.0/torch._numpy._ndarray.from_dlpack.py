def from_dlpack(x, /):
    t = torch.from_dlpack(x)
    return ndarray(t)
