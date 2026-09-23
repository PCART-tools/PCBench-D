@normalizer
@upcast
def ifftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.ifftn(a, s, dim=axes, norm=norm)
