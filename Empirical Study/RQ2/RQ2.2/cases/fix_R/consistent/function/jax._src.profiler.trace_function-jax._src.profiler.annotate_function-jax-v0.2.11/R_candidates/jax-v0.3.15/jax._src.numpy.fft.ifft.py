@_wraps(np.fft.ifft)
def ifft(a, n=None, axis=-1, norm=None):
  return _fft_core_1d('ifft', xla_client.FftType.IFFT, a, n=n, axis=axis,
                      norm=norm)
