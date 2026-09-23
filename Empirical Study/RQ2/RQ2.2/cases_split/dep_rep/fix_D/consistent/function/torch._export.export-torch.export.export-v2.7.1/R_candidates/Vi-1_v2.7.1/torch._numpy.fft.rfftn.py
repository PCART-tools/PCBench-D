@normalizer
@upcast
def rfftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.rfftn(a, s, dim=axes, norm=norm)
