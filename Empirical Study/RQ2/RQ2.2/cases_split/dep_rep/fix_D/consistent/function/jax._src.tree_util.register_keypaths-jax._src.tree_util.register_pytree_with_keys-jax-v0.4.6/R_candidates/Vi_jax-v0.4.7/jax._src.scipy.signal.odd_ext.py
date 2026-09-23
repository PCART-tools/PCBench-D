def odd_ext(x: Array, n: int, axis: int = -1) -> Array:
  """Extends `x` along with `axis` by odd-extension.

  This function was previously a part of "scipy.signal.signaltools" but is no
  longer exposed.

  Args:
    x : input array
    n : the number of points to be added to the both end
    axis: the axis to be extended
  """
  if n < 1:
    return x
  if n > x.shape[axis] - 1:
    raise ValueError(
        f"The extension length n ({n}) is too big. "
        f"It must not exceed x.shape[axis]-1, which is {x.shape[axis] - 1}.")
  left_end = lax.slice_in_dim(x, 0, 1, axis=axis)
  left_ext = jnp.flip(lax.slice_in_dim(x, 1, n + 1, axis=axis), axis=axis)
  right_end = lax.slice_in_dim(x, -1, None, axis=axis)
  right_ext = jnp.flip(lax.slice_in_dim(x, -(n + 1), -1, axis=axis), axis=axis)
  ext = jnp.concatenate((2 * left_end - left_ext,
                         x,
                         2 * right_end - right_ext),
                         axis=axis)
  return ext
