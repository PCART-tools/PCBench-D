def _spectral_helper(x, y,
                     fs=1.0, window='hann', nperseg=None, noverlap=None,
                     nfft=None, detrend_type='constant', return_onesided=True,
                     scaling='density', axis=-1, mode='psd', boundary=None,
                     padded=False):
  """LAX-backend implementation of `scipy.signal._spectral_helper`.

  Unlike the original helper function, `y` can be None for explicitly
  indicating auto-spectral (non cross-spectral) computation.  In addition to
  this, `detrend` argument is renamed to `detrend_type` for avoiding internal
  name overlap.
  """
  if mode not in ('psd', 'stft'):
    raise ValueError(f"Unknown value for mode {mode}, "
                     "must be one of: ('psd', 'stft')")

  def make_pad(mode, **kwargs):
    def pad(x, n, axis=-1):
      pad_width = [(0, 0) for unused_n in range(x.ndim)]
      pad_width[axis] = (n, n)
      return jnp.pad(x, pad_width, mode, **kwargs)
    return pad

  boundary_funcs = {
      'even': make_pad('reflect'),
      'odd': odd_ext,
      'constant': make_pad('edge'),
      'zeros': make_pad('constant', constant_values=0.0),
      None: lambda x, *args, **kwargs: x
  }

  # Check/ normalize inputs
  if boundary not in boundary_funcs:
    raise ValueError(
        f"Unknown boundary option '{boundary}', "
        f"must be one of: {list(boundary_funcs.keys())}")

  axis = jax.core.concrete_or_error(operator.index, axis,
                                    "axis of windowed-FFT")
  axis = canonicalize_axis(axis, x.ndim)

  if y is None:
    _check_arraylike('spectral_helper', x)
    x, = _promote_dtypes_inexact(x)
    outershape = tuple_delete(x.shape, axis)
  else:
    if mode != 'psd':
      raise ValueError("two-argument mode is available only when mode=='psd'")
    _check_arraylike('spectral_helper', x, y)
    x, y = _promote_dtypes_inexact(x, y)
    if x.ndim != y.ndim:
      raise ValueError("two-arguments must have the same rank ({x.ndim} vs {y.ndim}).")
    # Check if we can broadcast the outer axes together
    try:
      outershape = jnp.broadcast_shapes(tuple_delete(x.shape, axis),
                                        tuple_delete(y.shape, axis))
    except ValueError as err:
      raise ValueError('x and y cannot be broadcast together.') from err

  result_dtype = dtypes._to_complex_dtype(x.dtype)
  freq_dtype = np.finfo(result_dtype).dtype

  if nperseg is not None:  # if specified by user
    nperseg = jax.core.concrete_or_error(int, nperseg,
                                         "nperseg of windowed-FFT")
    if nperseg < 1:
      raise ValueError('nperseg must be a positive integer')
  # parse window; if array like, then set nperseg = win.shape
  win, nperseg = signal_helper._triage_segments(
      window, nperseg, input_length=x.shape[axis], dtype=x.dtype)

  if noverlap is None:
    noverlap = nperseg // 2
  else:
    noverlap = jax.core.concrete_or_error(int, noverlap,
                                          "noverlap of windowed-FFT")
  if nfft is None:
    nfft = nperseg
  else:
    nfft = jax.core.concrete_or_error(int, nfft,
                                      "nfft of windowed-FFT")

  # Special cases for size == 0
  if y is None:
    if x.size == 0:
      return jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, result_dtype)
  else:
    if x.size == 0 or y.size == 0:
      shape = tuple_insert(outershape, min([x.shape[axis], y.shape[axis]]), axis)
      return jnp.zeros(shape, freq_dtype), jnp.zeros(shape, freq_dtype), jnp.zeros(shape, result_dtype)

  # Move time-axis to the end
  x = jnp.moveaxis(x, axis, -1)
  if y is not None and y.ndim > 1:
    y = jnp.moveaxis(y, axis, -1)

  # Check if x and y are the same length, zero-pad if necessary
  if y is not None and x.shape[-1] != y.shape[-1]:
    if x.shape[-1] < y.shape[-1]:
      pad_shape = list(x.shape)
      pad_shape[-1] = y.shape[-1] - x.shape[-1]
      x = jnp.concatenate((x, jnp.zeros_like(x, shape=pad_shape)), -1)
    else:
      pad_shape = list(y.shape)
      pad_shape[-1] = x.shape[-1] - y.shape[-1]
      y = jnp.concatenate((y, jnp.zeros_like(x, shape=pad_shape)), -1)

  if nfft < nperseg:
    raise ValueError('nfft must be greater than or equal to nperseg.')
  if noverlap >= nperseg:
    raise ValueError('noverlap must be less than nperseg.')
  nstep = nperseg - noverlap

  # Apply paddings
  if boundary is not None:
    ext_func = boundary_funcs[boundary]
    x = ext_func(x, nperseg // 2, axis=-1)
    if y is not None:
      y = ext_func(y, nperseg // 2, axis=-1)

  if padded:
    # Pad to integer number of windowed segments
    # I.e make x.shape[-1] = nperseg + (nseg-1)*nstep, with integer nseg
    nadd = (-(x.shape[-1]-nperseg) % nstep) % nperseg
    x = jnp.concatenate((x, jnp.zeros_like(x, shape=(*x.shape[:-1], nadd))), axis=-1)
    if y is not None:
      y = jnp.concatenate((y, jnp.zeros_like(x, shape=(*y.shape[:-1], nadd))), axis=-1)

  # Handle detrending and window functions
  if not detrend_type:
    detrend_func = lambda d: d
  elif not callable(detrend_type):
    detrend_func = partial(detrend, type=detrend_type, axis=-1)
  elif axis != -1:
    # Wrap this function so that it receives a shape that it could
    # reasonably expect to receive.
    def detrend_func(d):
      d = jnp.moveaxis(d, axis, -1)
      d = detrend_type(d)
      return jnp.moveaxis(d, -1, axis)
  else:
    detrend_func = detrend_type

  # Determine scale
  if scaling == 'density':
    scale = 1.0 / (fs * (win * win).sum())
  elif scaling == 'spectrum':
    scale = 1.0 / win.sum()**2
  else:
    raise ValueError(f'Unknown scaling: {scaling}')
  if mode == 'stft':
    scale = jnp.sqrt(scale)
  scale, = _promote_dtypes_complex(scale)

  # Determine onesided/ two-sided
  if return_onesided:
    sides = 'onesided'
    if jnp.iscomplexobj(x) or jnp.iscomplexobj(y):
      sides = 'twosided'
      warnings.warn('Input data is complex, switching to '
                    'return_onesided=False')
  else:
    sides = 'twosided'

  if sides == 'twosided':
    freqs = jax.numpy.fft.fftfreq(nfft, 1/fs).astype(freq_dtype)
  elif sides == 'onesided':
    freqs = jax.numpy.fft.rfftfreq(nfft, 1/fs).astype(freq_dtype)

  # Perform the windowed FFTs
  result = _fft_helper(x, win, detrend_func,
                       nperseg, noverlap, nfft, sides)

  if y is not None:
    # All the same operations on the y data
    result_y = _fft_helper(y, win, detrend_func,
                           nperseg, noverlap, nfft, sides)
    result = jnp.conjugate(result) * result_y
  elif mode == 'psd':
    result = jnp.conjugate(result) * result

  result *= scale

  if sides == 'onesided' and mode == 'psd':
    end = None if nfft % 2 else -1
    result = result.at[..., 1:end].mul(2)

  time = jnp.arange(nperseg / 2, x.shape[-1] - nperseg / 2 + 1,
                    nperseg - noverlap, dtype=freq_dtype) / fs
  if boundary is not None:
    time -= (nperseg / 2) / fs

  result = result.astype(result_dtype)

  # All imaginary parts are zero anyways
  if y is None and mode != 'stft':
    result = result.real

  # Move frequency axis back to axis where the data came from
  result = jnp.moveaxis(result, -1, axis)

  return freqs, time, result
