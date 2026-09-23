@_wraps(np.fft.ifftn)
def ifftn(a: ArrayLike, s: Optional[Shape] = None,
          axes: Optional[Sequence[int]] = None,
          norm: Optional[str] = None) -> Array:
  return _fft_core('ifftn', xla_client.FftType.IFFT, a, s, axes, norm)
