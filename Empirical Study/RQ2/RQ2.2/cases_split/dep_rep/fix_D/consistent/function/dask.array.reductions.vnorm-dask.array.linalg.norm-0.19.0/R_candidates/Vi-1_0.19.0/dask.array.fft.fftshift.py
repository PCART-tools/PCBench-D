@wraps(np.fft.fftshift)
def fftshift(x, axes=None):
    return _fftshift_helper(x, axes=axes, inverse=False)
