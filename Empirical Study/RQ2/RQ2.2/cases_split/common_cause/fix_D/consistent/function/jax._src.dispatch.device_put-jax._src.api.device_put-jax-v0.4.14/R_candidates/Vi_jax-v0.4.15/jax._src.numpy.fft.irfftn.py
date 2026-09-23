@_wraps(np.fft.irfftn)
def irfftn(a: ArrayLike, s: Optional[Shape] = None,
           axes: Optional[Sequence[int]] = None,
           norm: Optional[str] = None) -> Array:
  return _fft_core('irfftn', xla_client.FftType.IRFFT, a, s, axes, norm)
