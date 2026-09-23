def _fft_core(func_name: str, fft_type: xla_client.FftType, a: ArrayLike,
              s: Shape | None, axes: Sequence[int] | None,
              norm: str | None) -> Array:
  full_name = f"jax.numpy.fft.{func_name}"
  check_arraylike(full_name, a)
  arr = jnp.asarray(a)

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
      axes = range(arr.ndim)
    else:
      axes = range(arr.ndim - len(s), arr.ndim)

  if len(axes) != len(set(axes)):
    raise ValueError(
        f"{full_name} does not support repeated axes. Got axes {axes}.")

  if len(axes) > 3:
    # XLA does not support FFTs over more than 3 dimensions
    raise ValueError(
        "%s only supports 1D, 2D, and 3D FFTs. "
        "Got axes %s with input rank %s." % (full_name, orig_axes, arr.ndim))

  # XLA only supports FFTs over the innermost axes, so rearrange if necessary.
  if orig_axes is not None:
    axes = tuple(range(arr.ndim - len(axes), arr.ndim))
    arr = jnp.moveaxis(arr, orig_axes, axes)

  if s is not None:
    in_s = list(arr.shape)
    for axis, x in safe_zip(axes, s):
      in_s[axis] = x
    if fft_type == xla_client.FftType.IRFFT:
      in_s[-1] = (in_s[-1] // 2 + 1)
    # Cropping
    arr = arr[tuple(map(slice, in_s))]
    # Padding
    arr = jnp.pad(arr, [(0, x-y) for x, y in zip(in_s, arr.shape)])
  else:
    if fft_type == xla_client.FftType.IRFFT:
      s = [arr.shape[axis] for axis in axes[:-1]]
      if axes:
        s += [max(0, 2 * (arr.shape[axes[-1]] - 1))]
    else:
      s = [arr.shape[axis] for axis in axes]
  transformed = lax.fft(arr, fft_type, tuple(s))
  if norm is not None:
    transformed *= _fft_norm(
        jnp.array(s, dtype=transformed.dtype), func_name, norm)

  if orig_axes is not None:
    transformed = jnp.moveaxis(transformed, axes, orig_axes)
  return transformed
