@_wraps(np.fft.irfft2)
def irfft2(a: ArrayLike, s: Optional[Shape] = None, axes: Sequence[int] = (-2,-1),
           norm: Optional[str] = None) -> Array:
  return _fft_core_2d('irfft2', xla_client.FftType.IRFFT, a, s=s, axes=axes,
                      norm=norm)
