@_wraps(osp_signal.stft)
def stft(x: Array, fs: ArrayLike = 1.0, window: str = 'hann', nperseg: int = 256,
         noverlap: Optional[int] = None, nfft: Optional[int] = None,
         detrend: bool = False, return_onesided: bool = True, boundary: Optional[str] = 'zeros',
         padded: bool = True, axis: int = -1) -> Tuple[Array, Array, Array]:
  return _spectral_helper(x, None, fs, window, nperseg, noverlap,
                          nfft, detrend, return_onesided,
                          scaling='spectrum', axis=axis,
                          mode='stft', boundary=boundary,
                          padded=padded)
