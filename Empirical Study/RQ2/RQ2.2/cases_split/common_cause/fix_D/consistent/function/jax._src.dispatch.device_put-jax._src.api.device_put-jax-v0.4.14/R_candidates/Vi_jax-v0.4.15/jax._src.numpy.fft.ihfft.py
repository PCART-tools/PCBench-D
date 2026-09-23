@_wraps(np.fft.ihfft)
def ihfft(a: ArrayLike, n: Optional[int] = None,
          axis: int = -1, norm: Optional[str] = None) -> Array:
  _axis_check_1d('ihfft', axis)
  arr = jnp.asarray(a)
  nn = arr.shape[axis] if n is None else n
  output = _fft_core_1d('ihfft', xla_client.FftType.RFFT, arr, n=n, axis=axis,
                        norm=norm)
  return ufuncs.conj(output) * (1 / nn)
