@normalizer
@upcast
def fft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.fft(a, n, dim=axis, norm=norm)
