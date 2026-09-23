@_wraps(np.fft.irfft)
def irfft(a, n=None, axis=-1, norm=None):
  return _fft_core_1d('irfft', xla_client.FftType.IRFFT, a, n=n, axis=axis,
                      norm=norm)
