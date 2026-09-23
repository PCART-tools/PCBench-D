@implements(np.fft.fft)
def fft(a: ArrayLike, n: int | None = None,
        axis: int = -1, norm: str | None = None) -> Array:
  return _fft_core_1d('fft', xla_client.FftType.FFT, a, n=n, axis=axis,
                      norm=norm)
