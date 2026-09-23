def _spectral_helper(x: Array, y: ArrayLike | None, fs: ArrayLike = 1.0,
                     window: str = 'hann', nperseg: int | None = None,
                     noverlap: int | None = None, nfft: int | None = None,
                     detrend_type: bool | str | Callable[[Array], Array] = 'constant',
                     return_onesided: bool = True, scaling: str = 'density',
                     axis: int = -1, mode: str = 'psd', boundary: str | None = None,
                     padded: bool = False) -> tuple[Array, Array, Array]:
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
    check_arraylike('spectral_helper', x)
    x, = promote_dtypes_inexact(x)
    y_arr = x  # place-holder for type checking
    outershape = tuple_delete(x.shape, axis)
  else:
    if mode != 'psd':
      raise ValueError("two-argument mode is available only when mode=='psd'")
    check_arraylike('spectral_helper', x, y)
    x, y_arr = promote_dtypes_inexact(x, y)
    if x.ndim != y_arr.ndim:
      raise ValueError("two-arguments must have the same rank ({x.ndim} vs {y.ndim}).")
    # Check if we can broadcast the outer axes together
    try:
      outershape = jnp.broadcast_shapes(tuple_delete(x.shape, axis),
                                        tuple_delete(y_arr.shape, axis))
    except ValueError as err:
      raise ValueError('x and y cannot be broadcast together.') from err

  result_dtype = dtypes.to_complex_dtype(x.dtype)
  freq_dtype = np.finfo(result_dtype).dtype

  nperseg_int: int = 0
  nfft_int: int = 0
  noverlap_int: int = 0

  if nperseg is not None:  # if specified by user
    nperseg_int = jax.core.concrete_or_error(int, nperseg,
                                             "nperseg of windowed-FFT")
    if nperseg_int < 1:  # type: ignore[operator]
      raise ValueError('nperseg must be a positive integer')
  # parse window; if array like, then set nperseg = win.shape
  win, nperseg_int = signal_helper._triage_segments(
      window, nperseg if nperseg is None else nperseg_int,
      input_length=x.shape[axis], dtype=x.dtype)

  if noverlap is None:
    noverlap_int = nperseg_int // 2  # type: ignore[operator]
  else:
    noverlap_int = jax.core.concrete_or_error(int, noverlap,
                                              "noverlap of windowed-FFT")

  if nfft is None:
    nfft_int = nperseg_int
  else:
    nfft_int = jax.core.concrete_or_error(int, nfft,
                                          "nfft of windowed-FFT")

  # Special cases for size == 0
  if y is None:
    if x.size == 0:
      return jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, freq_dtype), jnp.zeros(x.shape, result_dtype)
  else:
    if x.size == 0 or y_arr.size == 0:
      shape = tuple_insert(outershape, min([x.shape[axis], y_arr.shape[axis]]), axis)
      return jnp.zeros(shape, freq_dtype), jnp.zeros(shape, freq_dtype), jnp.zeros(shape, result_dtype)

  # Move time-axis to the end
  x = jnp.moveaxis(x, axis, -1)
  if y is not None and y_arr.ndim > 1:
    y_arr = jnp.moveaxis(y_arr, axis, -1)

  # Check if x and y are the same length, zero-pad if necessary
  if y is not None and x.shape[-1] != y_arr.shape[-1]:
    if x.shape[-1] < y_arr.shape[-1]:
      pad_shape = list(x.shape)
      pad_shape[-1] = y_arr.shape[-1] - x.shape[-1]
      x = jnp.concatenate((x, jnp.zeros_like(x, shape=pad_shape)), -1)
    else:
      pad_shape = list(y_arr.shape)
      pad_shape[-1] = x.shape[-1] - y_arr.shape[-1]
      y_arr = jnp.concatenate((y_arr, jnp.zeros_like(x, shape=pad_shape)), -1)

  if nfft_int < nperseg_int:
    raise ValueError('nfft must be greater than or equal to nperseg.')
  if noverlap_int >= nperseg_int:
    raise ValueError('noverlap must be less than nperseg.')
  nstep = nperseg_int - noverlap_int

  # Apply paddings
  if boundary is not None:
    ext_func = boundary_funcs[boundary]
    x = ext_func(x, nperseg_int // 2, axis=-1)
    if y is not None:
      y_arr = ext_func(y_arr, nperseg_int // 2, axis=-1)

  if padded:
    # Pad to integer number of windowed segments
    # I.e make x.shape[-1] = nperseg + (nseg-1)*nstep, with integer nseg
    nadd = (-(x.shape[-1]-nperseg_int) % nstep) % nperseg_int
    x = jnp.concatenate((x, jnp.zeros_like(x, shape=(*x.shape[:-1], nadd))), axis=-1)
    if y is not None:
      y_arr = jnp.concatenate((y_arr, jnp.zeros_like(x, shape=(*y_arr.shape[:-1], nadd))), axis=-1)

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
  scale, = promote_dtypes_complex(scale)

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
    freqs = jax.numpy.fft.fftfreq(nfft_int, 1/fs, dtype=freq_dtype)
  elif sides == 'onesided':
    freqs = jax.numpy.fft.rfftfreq(nfft_int, 1/fs, dtype=freq_dtype)

  # Perform the windowed FFTs
  result = _fft_helper(x, win, detrend_func,
                       nperseg_int, noverlap_int, nfft_int, sides)

  if y is not None:
    # All the same operations on the y data
    result_y = _fft_helper(y_arr, win, detrend_func,
                           nperseg_int, noverlap_int, nfft_int, sides)
    result = jnp.conjugate(result) * result_y
  elif mode == 'psd':
    result = jnp.conjugate(result) * result

  result *= scale

  if sides == 'onesided' and mode == 'psd':
    end = None if nfft_int % 2 else -1
    result = result.at[..., 1:end].mul(2)

  time = jnp.arange(nperseg_int / 2, x.shape[-1] - nperseg_int / 2 + 1,
                    nperseg_int - noverlap_int, dtype=freq_dtype) / fs
  if boundary is not None:
    time -= (nperseg_int / 2) / fs

  result = result.astype(result_dtype)

  # All imaginary parts are zero anyways
  if y is None and mode != 'stft':
    result = result.real

  # Move frequency axis back to axis where the data came from
  result = jnp.moveaxis(result, -1, axis)

  return freqs, time, result
