@implements(osp_signal.welch)
def welch(x: Array, fs: ArrayLike = 1.0, window: str = 'hann',
          nperseg: int | None = None, noverlap: int | None = None,
          nfft: int | None = None, detrend: str = 'constant',
          return_onesided: bool = True, scaling: str = 'density',
          axis: int = -1, average: str = 'mean') -> tuple[Array, Array]:
  freqs, Pxx = csd(x, None, fs=fs, window=window, nperseg=nperseg,
                   noverlap=noverlap, nfft=nfft, detrend=detrend,
                   return_onesided=return_onesided, scaling=scaling,
                   axis=axis, average=average)

  return freqs, Pxx.real
