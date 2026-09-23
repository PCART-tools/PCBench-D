@normalizer
def ifftshift(x: ArrayLike, axes=None):
    return torch.fft.ifftshift(x, axes)
