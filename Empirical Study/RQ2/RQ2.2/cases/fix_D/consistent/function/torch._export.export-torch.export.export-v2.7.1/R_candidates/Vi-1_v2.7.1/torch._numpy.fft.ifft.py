@normalizer
@upcast
def ifft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.ifft(a, n, dim=axis, norm=norm)
