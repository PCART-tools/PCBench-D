@_wraps(np.fft.fft)
def fft(a: ArrayLike, n: Optional[int] = None,
        axis: int = -1, norm: Optional[str] = None) -> Array:
  return _fft_core_1d('fft', xla_client.FftType.FFT, a, n=n, axis=axis,
                      norm=norm)
