@_wraps(osp_signal.csd, lax_description=_csd_description)
def csd(x, y, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None,
        detrend='constant', return_onesided=True, scaling='density',
        axis=-1, average='mean'):
  freqs, _, Pxy = _spectral_helper(x, y, fs, window, nperseg, noverlap, nfft,
                                  detrend, return_onesided, scaling, axis,
                                  mode='psd')
  if y is not None:
    Pxy = Pxy + 0j  # Ensure complex output when x is not y

  # Average over windows.
  if Pxy.ndim >= 2 and Pxy.size > 0:
    if Pxy.shape[-1] > 1:
      if average == 'median':
        bias = signal_helper._median_bias(Pxy.shape[-1]).astype(Pxy.dtype)
        if jnp.iscomplexobj(Pxy):
          Pxy = (jnp.median(jnp.real(Pxy), axis=-1)
                  + 1j * jnp.median(jnp.imag(Pxy), axis=-1))
        else:
          Pxy = jnp.median(Pxy, axis=-1)
        Pxy /= bias
      elif average == 'mean':
        Pxy = Pxy.mean(axis=-1)
      else:
        raise ValueError(f'average must be "median" or "mean", got {average}')
    else:
      Pxy = jnp.reshape(Pxy, Pxy.shape[:-1])

  return freqs, Pxy
