@normalizer
@upcast
def rfft(a: ArrayLike, n=None, axis=-1, norm=None):
    return torch.fft.rfft(a, n, dim=axis, norm=norm)
