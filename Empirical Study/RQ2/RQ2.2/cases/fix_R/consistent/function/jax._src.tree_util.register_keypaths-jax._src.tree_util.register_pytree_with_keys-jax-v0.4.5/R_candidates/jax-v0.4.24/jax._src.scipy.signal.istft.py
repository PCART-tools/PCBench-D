@implements(osp_signal.istft)
def istft(Zxx: Array, fs: ArrayLike = 1.0, window: str = 'hann',
          nperseg: int | None = None, noverlap: int | None = None,
          nfft: int | None = None, input_onesided: bool = True,
          boundary: bool = True, time_axis: int = -1,
          freq_axis: int = -2) -> tuple[Array, Array]:
  # Input validation
  check_arraylike("istft", Zxx)
  if Zxx.ndim < 2:
    raise ValueError('Input stft must be at least 2d!')
  freq_axis = canonicalize_axis(freq_axis, Zxx.ndim)
  time_axis = canonicalize_axis(time_axis, Zxx.ndim)
  if freq_axis == time_axis:
    raise ValueError('Must specify differing time and frequency axes!')

  Zxx = jnp.asarray(Zxx, dtype=jax.dtypes.canonicalize_dtype(
      np.result_type(Zxx, np.complex64)))

  n_default = (2 * (Zxx.shape[freq_axis] - 1) if input_onesided
               else Zxx.shape[freq_axis])

  nperseg_int = jax.core.concrete_or_error(int, nperseg or n_default,
                                           "nperseg: segment length of STFT")
  if nperseg_int < 1:
    raise ValueError('nperseg must be a positive integer')

  nfft_int: int = 0
  if nfft is None:
    nfft_int = n_default
    if input_onesided and nperseg_int == n_default + 1:
      nfft_int += 1  # Odd nperseg, no FFT padding
  else:
    nfft_int = jax.core.concrete_or_error(int, nfft, "nfft of STFT")
  if nfft_int < nperseg_int:
    raise ValueError(
        f'FFT length ({nfft_int}) must be longer than nperseg ({nperseg_int}).')

  noverlap_int = jax.core.concrete_or_error(int, noverlap or nperseg_int // 2,
                                            "noverlap of STFT")
  if noverlap_int >= nperseg_int:
    raise ValueError('noverlap must be less than nperseg.')
  nstep = nperseg_int - noverlap_int

  # Rearrange axes if necessary
  if time_axis != Zxx.ndim - 1 or freq_axis != Zxx.ndim - 2:
    outer_idxs = tuple(
        idx for idx in range(Zxx.ndim) if idx not in {time_axis, freq_axis})
    Zxx = jnp.transpose(Zxx, outer_idxs + (freq_axis, time_axis))

  # Perform IFFT
  ifunc = jax.numpy.fft.irfft if input_onesided else jax.numpy.fft.ifft
  # xsubs: [..., T, N], N is the number of frames, T is the frame length.
  xsubs = ifunc(Zxx, axis=-2, n=nfft)[..., :nperseg_int, :]

  # Get window as array
  if isinstance(window, (str, tuple)):
    win = osp_signal.get_window(window, nperseg_int)
    win = jnp.asarray(win, dtype=xsubs.dtype)
  else:
    win = jnp.asarray(window)
    if len(win.shape) != 1:
      raise ValueError('window must be 1-D')
    if win.shape[0] != nperseg_int:
      raise ValueError(f'window must have length of {nperseg_int}')
  xsubs *= win.sum()  # This takes care of the 'spectrum' scaling

  # make win broadcastable over xsubs
  win = lax.expand_dims(win, (*range(xsubs.ndim - 2), -1))
  x = _overlap_and_add((xsubs * win).swapaxes(-2, -1), nstep)
  win_squared = jnp.repeat((win * win), xsubs.shape[-1], axis=-1)
  norm = _overlap_and_add(win_squared.swapaxes(-2, -1), nstep)

  # Remove extension points
  if boundary:
    x = x[..., nperseg_int//2:-(nperseg_int//2)]
    norm = norm[..., nperseg_int//2:-(nperseg_int//2)]
  x /= jnp.where(norm > 1e-10, norm, 1.0)

  # Put axes back
  if x.ndim > 1:
    if time_axis != Zxx.ndim - 1:
      if freq_axis < time_axis:
        time_axis -= 1
      x = jnp.moveaxis(x, -1, time_axis)

  time = jnp.arange(x.shape[0], dtype=np.finfo(x.dtype).dtype) / fs
  return time, x
