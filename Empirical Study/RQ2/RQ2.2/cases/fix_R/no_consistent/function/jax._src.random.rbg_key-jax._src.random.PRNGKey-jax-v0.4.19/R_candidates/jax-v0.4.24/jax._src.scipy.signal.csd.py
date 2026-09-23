@implements(osp_signal.csd, lax_description=_csd_description)
def csd(x: Array, y: ArrayLike | None, fs: ArrayLike = 1.0, window: str = 'hann',
        nperseg: int | None = None, noverlap: int | None = None,
        nfft: int | None = None, detrend: str = 'constant',
        return_onesided: bool = True, scaling: str = 'density',
        axis: int = -1, average: str = 'mean') -> tuple[Array, Array]:
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
