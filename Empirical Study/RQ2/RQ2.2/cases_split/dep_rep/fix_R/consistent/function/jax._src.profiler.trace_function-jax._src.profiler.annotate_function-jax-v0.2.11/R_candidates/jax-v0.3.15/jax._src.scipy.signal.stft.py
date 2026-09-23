@_wraps(osp_signal.stft)
def stft(x, fs=1.0, window='hann', nperseg=256, noverlap=None, nfft=None,
         detrend=False, return_onesided=True, boundary='zeros', padded=True,
         axis=-1):
  return _spectral_helper(x, None, fs, window, nperseg, noverlap,
                          nfft, detrend, return_onesided,
                          scaling='spectrum', axis=axis,
                          mode='stft', boundary=boundary,
                          padded=padded)
