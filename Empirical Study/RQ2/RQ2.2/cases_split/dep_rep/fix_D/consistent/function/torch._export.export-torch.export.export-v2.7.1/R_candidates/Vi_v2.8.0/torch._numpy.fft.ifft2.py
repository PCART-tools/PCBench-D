@normalizer
@upcast
def ifft2(a: ArrayLike, s=None, axes=(-2, -1), norm=None):
    return torch.fft.ifft2(a, s, dim=axes, norm=norm)
