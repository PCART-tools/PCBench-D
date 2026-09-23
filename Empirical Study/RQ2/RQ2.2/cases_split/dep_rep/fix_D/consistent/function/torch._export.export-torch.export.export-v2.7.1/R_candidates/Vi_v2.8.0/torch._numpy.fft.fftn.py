@normalizer
@upcast
def fftn(a: ArrayLike, s=None, axes=None, norm=None):
    return torch.fft.fftn(a, s, dim=axes, norm=norm)
