@normalizer
@upcast
def irfft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.irfft2(a, s, dim=axes, norm=norm)
