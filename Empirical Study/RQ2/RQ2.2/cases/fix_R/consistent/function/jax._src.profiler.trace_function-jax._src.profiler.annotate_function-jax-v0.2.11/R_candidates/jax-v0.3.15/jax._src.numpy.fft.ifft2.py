@_wraps(np.fft.ifft2)
def ifft2(a, s=None, axes=(-2,-1), norm=None):
  return _fft_core_2d('ifft2', xla_client.FftType.IFFT, a, s=s, axes=axes,
                      norm=norm)
