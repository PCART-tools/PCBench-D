@implements(np.fft.ifftn)
def ifftn(a: ArrayLike, s: Shape | None = None,
          axes: Sequence[int] | None = None,
          norm: str | None = None) -> Array:
  return _fft_core('ifftn', xla_client.FftType.IFFT, a, s, axes, norm)
