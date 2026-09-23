@normalizer
@upcast
def irfftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.irfftn(a, s, dim=axes, norm=norm)
