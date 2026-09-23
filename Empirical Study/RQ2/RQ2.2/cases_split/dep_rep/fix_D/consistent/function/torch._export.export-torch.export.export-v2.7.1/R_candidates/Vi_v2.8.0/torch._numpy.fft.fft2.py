@normalizer
@upcast
def fft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.fft2(a, s, dim=axes, norm=norm)
