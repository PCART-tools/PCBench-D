@_wraps(np.fft.rfftn)
def rfftn(a: ArrayLike, s: Optional[Shape] = None,
          axes: Optional[Sequence[int]] = None,
          norm: Optional[str] = None) -> Array:
  return _fft_core('rfftn', xla_client.FftType.RFFT, a, s, axes, norm)
