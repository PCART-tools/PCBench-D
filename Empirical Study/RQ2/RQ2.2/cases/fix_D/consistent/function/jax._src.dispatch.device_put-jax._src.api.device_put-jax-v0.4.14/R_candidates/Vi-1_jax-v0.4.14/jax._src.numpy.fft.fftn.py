@_wraps(np.fft.fftn)
def fftn(a: ArrayLike, s: Optional[Shape] = None,
         axes: Optional[Sequence[int]] = None,
         norm: Optional[str] = None) -> Array:
  return _fft_core('fftn', xla_client.FftType.FFT, a, s, axes, norm)
