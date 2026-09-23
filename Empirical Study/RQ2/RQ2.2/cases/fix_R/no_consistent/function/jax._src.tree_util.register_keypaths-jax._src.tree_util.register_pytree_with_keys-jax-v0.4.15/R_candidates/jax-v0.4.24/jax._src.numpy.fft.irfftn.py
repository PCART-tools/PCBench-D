@implements(np.fft.irfftn)
def irfftn(a: ArrayLike, s: Shape | None = None,
           axes: Sequence[int] | None = None,
           norm: str | None = None) -> Array:
  return _fft_core('irfftn', xla_client.FftType.IRFFT, a, s, axes, norm)
