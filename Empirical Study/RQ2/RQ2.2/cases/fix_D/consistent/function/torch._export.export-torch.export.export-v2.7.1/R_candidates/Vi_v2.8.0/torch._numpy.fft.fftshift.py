@normalizer
def fftshift(x: ArrayLike, axes=None):
    return torch.fft.fftshift(x, axes)
