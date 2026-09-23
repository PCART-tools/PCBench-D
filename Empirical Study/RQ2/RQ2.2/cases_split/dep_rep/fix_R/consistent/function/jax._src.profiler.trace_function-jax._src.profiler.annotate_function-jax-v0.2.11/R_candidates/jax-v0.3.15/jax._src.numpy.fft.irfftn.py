@_wraps(np.fft.irfftn)
def irfftn(a, s=None, axes=None, norm=None):
  return _fft_core('irfftn', xla_client.FftType.IRFFT, a, s, axes, norm)
