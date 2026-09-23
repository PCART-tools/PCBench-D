def imag(a: ArrayLike):
    if a.is_complex():
        return a.imag
    return torch.zeros_like(a)
