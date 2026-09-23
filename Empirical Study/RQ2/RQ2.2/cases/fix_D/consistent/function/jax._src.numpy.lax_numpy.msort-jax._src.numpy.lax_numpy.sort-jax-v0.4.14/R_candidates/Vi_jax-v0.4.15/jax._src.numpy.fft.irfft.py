@_wraps(np.fft.irfft)
def irfft(a: ArrayLike, n: Optional[int] = None,
          axis: int = -1, norm: Optional[str] = None) -> Array:
  return _fft_core_1d('irfft', xla_client.FftType.IRFFT, a, n=n, axis=axis,
                      norm=norm)
