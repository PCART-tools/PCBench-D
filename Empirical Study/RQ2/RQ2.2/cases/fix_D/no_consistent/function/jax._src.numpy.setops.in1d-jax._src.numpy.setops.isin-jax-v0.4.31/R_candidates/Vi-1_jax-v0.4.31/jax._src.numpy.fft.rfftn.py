@implements(np.fft.rfftn)
def rfftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  return _fft_core('rfftn', xla_client.FftType.RFFT, a, s, axes, norm)
