@_wraps(np.fft.ifft2)
def ifft2(a: ArrayLike, s: Optional[Shape] = None, axes: Sequence[int] = (-2,-1),
          norm: Optional[str] = None) -> Array:
  return _fft_core_2d('ifft2', xla_client.FftType.IFFT, a, s=s, axes=axes,
                      norm=norm)
