@_wraps(np.fft.fft)
def fft(a, n=None, axis=-1, norm=None):
  return _fft_core_1d('fft', xla_client.FftType.FFT, a, n=n, axis=axis,
                      norm=norm)
