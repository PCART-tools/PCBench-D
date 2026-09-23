def _fft_helper(x: Array, win: Array, detrend_func: Callable[[Array], Array],
                nperseg: int, noverlap: int, nfft: Optional[int], sides: str) -> Array:
  """Calculate windowed FFT in the same way the original SciPy does.
  """
  if x.dtype.kind == 'i':
    x = x.astype(win.dtype)

  *batch_shape, signal_length = x.shape
  # Created strided array of data segments
  if nperseg == 1 and noverlap == 0:
    result = x[..., np.newaxis]
  else:
    step = nperseg - noverlap
    batch_shape = list(batch_shape)
    x = x.reshape((int(np.prod(batch_shape)), signal_length))[..., np.newaxis]
    result = jax.lax.conv_general_dilated_patches(
        x, (nperseg,), (step,),
        'VALID',
        dimension_numbers=('NTC', 'OIT', 'NTC'))
    result = result.reshape(*batch_shape, *result.shape[-2:])

  # Detrend each data segment individually
  result = detrend_func(result)

  # Apply window by multiplication
  if jnp.iscomplexobj(win):
    result, = _promote_dtypes_complex(result)
  result = win.reshape((1,) * len(batch_shape) + (1, nperseg)) * result

  # Perform the fft on last axis. Zero-pads automatically
  if sides == 'twosided':
    return jax.numpy.fft.fft(result, n=nfft)
  else:
    return jax.numpy.fft.rfft(result.real, n=nfft)
