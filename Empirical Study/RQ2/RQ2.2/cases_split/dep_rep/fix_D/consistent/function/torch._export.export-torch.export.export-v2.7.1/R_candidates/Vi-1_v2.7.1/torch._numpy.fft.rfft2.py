@normalizer
@upcast
def rfft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.rfft2(a, s, dim=axes, norm=norm)
