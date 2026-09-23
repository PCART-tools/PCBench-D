@_wraps(np.fft.rfft)
def rfft(a: ArrayLike, n: Optional[int] = None,
         axis: int = -1, norm: Optional[str] = None) -> Array:
  return _fft_core_1d('rfft', xla_client.FftType.RFFT, a, n=n, axis=axis,
                      norm=norm)
