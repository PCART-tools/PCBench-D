@normalizer
@upcast
def hfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.hfft(a, n, dim=axis, norm=norm)
