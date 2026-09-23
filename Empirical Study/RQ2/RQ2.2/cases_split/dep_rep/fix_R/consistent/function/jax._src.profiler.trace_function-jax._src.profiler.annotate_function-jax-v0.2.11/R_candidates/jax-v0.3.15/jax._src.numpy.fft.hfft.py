@_wraps(np.fft.hfft)
def hfft(a, n=None, axis=-1, norm=None):
  conj_a = jnp.conj(a)
  _axis_check_1d('hfft', axis)
  nn = (a.shape[axis] - 1) * 2 if n is None else n
  return _fft_core_1d('hfft', xla_client.FftType.IRFFT, conj_a, n=n, axis=axis,
                      norm=norm) * nn
