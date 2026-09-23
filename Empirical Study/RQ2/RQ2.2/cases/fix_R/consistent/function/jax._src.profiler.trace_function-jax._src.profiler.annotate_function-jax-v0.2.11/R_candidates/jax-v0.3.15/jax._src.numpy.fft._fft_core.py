def _fft_core(func_name, fft_type, a, s, axes, norm):
  full_name = "jax.numpy.fft." + func_name

  if s is not None:
    s = tuple(map(operator.index, s))
    if np.any(np.less(s, 0)):
      raise ValueError("Shape should be non-negative.")

  if s is not None and axes is not None and len(s) != len(axes):
    # Same error as numpy.
    raise ValueError("Shape and axes have different lengths.")

  orig_axes = axes
  if axes is None:
    if s is None:
      axes = range(a.ndim)
    else:
      axes = range(a.ndim - len(s), a.ndim)

  if len(axes) != len(set(axes)):
    raise ValueError(
        f"{full_name} does not support repeated axes. Got axes {axes}.")

  if len(axes) > 3:
    # XLA does not support FFTs over more than 3 dimensions
    raise ValueError(
        "%s only supports 1D, 2D, and 3D FFTs. "
        "Got axes %s with input rank %s." % (full_name, orig_axes, a.ndim))

  # XLA only supports FFTs over the innermost axes, so rearrange if necessary.
  if orig_axes is not None:
    axes = tuple(range(a.ndim - len(axes), a.ndim))
    a = jnp.moveaxis(a, orig_axes, axes)

  if s is not None:
    a = jnp.asarray(a)
    in_s = list(a.shape)
    for axis, x in safe_zip(axes, s):
      in_s[axis] = x
    if fft_type == xla_client.FftType.IRFFT:
      in_s[-1] = (in_s[-1] // 2 + 1)
    # Cropping
    a = a[tuple(map(slice, in_s))]
    # Padding
    a = jnp.pad(a, [(0, x-y) for x, y in zip(in_s, a.shape)])
  else:
    if fft_type == xla_client.FftType.IRFFT:
      s = [a.shape[axis] for axis in axes[:-1]]
      if axes:
        s += [max(0, 2 * (a.shape[axes[-1]] - 1))]
    else:
      s = [a.shape[axis] for axis in axes]
  transformed = lax.fft(a, fft_type, tuple(s))
  if norm is not None:
    transformed *= _fft_norm(
        jnp.array(s, dtype=transformed.dtype), func_name, norm)

  if orig_axes is not None:
    transformed = jnp.moveaxis(transformed, axes, orig_axes)
  return transformed
