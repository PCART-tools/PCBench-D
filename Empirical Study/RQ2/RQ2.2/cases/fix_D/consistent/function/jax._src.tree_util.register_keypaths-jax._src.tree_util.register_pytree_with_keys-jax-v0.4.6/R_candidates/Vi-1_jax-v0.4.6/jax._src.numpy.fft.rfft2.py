@_wraps(np.fft.rfft2)
def rfft2(a: ArrayLike, s: Optional[Shape] = None, axes: Sequence[int] = (-2,-1),
          norm: Optional[str] = None) -> Array:
  return _fft_core_2d('rfft2', xla_client.FftType.RFFT, a, s=s, axes=axes,
                      norm=norm)
