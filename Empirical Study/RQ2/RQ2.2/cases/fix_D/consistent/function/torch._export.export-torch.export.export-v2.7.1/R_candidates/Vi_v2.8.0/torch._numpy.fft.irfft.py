@normalizer
@upcast
def irfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.irfft(a, n, dim=axis, norm=norm)
