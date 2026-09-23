@_wraps(np.fft.fft2)
def fft2(a: ArrayLike, s: Optional[Shape] = None, axes: Sequence[int] = (-2,-1),
         norm: Optional[str] = None) -> Array:
  return _fft_core_2d('fft2', xla_client.FftType.FFT, a, s=s, axes=axes,
                      norm=norm)
