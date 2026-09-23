@implements(np.fft.ifft)
def ifft(a: ArrayLike, n: int | None = None,
         axis: int = -1, norm: str | None = None) -> Array:
  return _fft_core_1d('ifft', xla_client.FftType.IFFT, a, n=n, axis=axis,
                      norm=norm)
