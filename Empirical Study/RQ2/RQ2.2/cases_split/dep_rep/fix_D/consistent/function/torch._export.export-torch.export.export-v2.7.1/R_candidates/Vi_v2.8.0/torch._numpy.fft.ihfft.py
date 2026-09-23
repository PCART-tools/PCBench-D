@normalizer
@upcast
def ihfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.ihfft(a, n, dim=axis, norm=norm)
