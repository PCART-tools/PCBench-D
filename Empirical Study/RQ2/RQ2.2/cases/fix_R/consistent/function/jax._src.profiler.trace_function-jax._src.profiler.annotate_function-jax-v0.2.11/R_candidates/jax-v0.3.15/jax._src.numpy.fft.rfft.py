@_wraps(np.fft.rfft)
def rfft(a, n=None, axis=-1, norm=None):
  return _fft_core_1d('rfft', xla_client.FftType.RFFT, a, n=n, axis=axis,
                      norm=norm)
