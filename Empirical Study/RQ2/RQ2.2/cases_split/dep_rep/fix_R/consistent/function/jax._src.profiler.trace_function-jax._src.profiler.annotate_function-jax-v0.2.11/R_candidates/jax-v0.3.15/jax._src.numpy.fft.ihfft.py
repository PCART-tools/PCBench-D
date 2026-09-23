@_wraps(np.fft.ihfft)
def ihfft(a, n=None, axis=-1, norm=None):
  _axis_check_1d('ihfft', axis)
  nn = a.shape[axis] if n is None else n
  output = _fft_core_1d('ihfft', xla_client.FftType.RFFT, a, n=n, axis=axis,
                      norm=norm)
  return jnp.conj(output) * (1 / nn)
