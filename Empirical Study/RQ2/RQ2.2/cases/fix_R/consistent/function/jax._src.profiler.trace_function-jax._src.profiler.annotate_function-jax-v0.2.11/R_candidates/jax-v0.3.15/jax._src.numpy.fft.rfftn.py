@_wraps(np.fft.rfftn)
def rfftn(a, s=None, axes=None, norm=None):
  return _fft_core('rfftn', xla_client.FftType.RFFT, a, s, axes, norm)
