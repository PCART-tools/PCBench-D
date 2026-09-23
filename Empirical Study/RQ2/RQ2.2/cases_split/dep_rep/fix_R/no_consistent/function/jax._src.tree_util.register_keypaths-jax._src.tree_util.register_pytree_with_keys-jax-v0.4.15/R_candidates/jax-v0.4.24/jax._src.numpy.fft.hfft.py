@implements(np.fft.hfft)
def hfft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  conj_a = ufuncs.conj(a)
  _axis_check_1d('hfft', axis)
  nn = (conj_a.shape[axis] - 1) * 2 if n is None else n
  return _fft_core_1d('hfft', xla_client.FftType.IRFFT, conj_a, n=n, axis=axis,
                      norm=norm) * nn
