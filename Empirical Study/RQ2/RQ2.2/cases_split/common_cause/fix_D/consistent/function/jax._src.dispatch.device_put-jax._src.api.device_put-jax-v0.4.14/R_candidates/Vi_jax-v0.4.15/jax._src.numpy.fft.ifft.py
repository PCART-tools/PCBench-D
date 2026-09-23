@_wraps(np.fft.ifft)
def ifft(a: ArrayLike, n: Optional[int] = None,
         axis: int = -1, norm: Optional[str] = None) -> Array:
  return _fft_core_1d('ifft', xla_client.FftType.IFFT, a, n=n, axis=axis,
                      norm=norm)
