@implements(np.fft.fftn)
def fftn(a: ArrayLike, s: Shape | None = None,
         axes: Sequence[int] | None = None,
         norm: str | None = None) -> Array:
  return _fft_core('fftn', xla_client.FftType.FFT, a, s, axes, norm)
