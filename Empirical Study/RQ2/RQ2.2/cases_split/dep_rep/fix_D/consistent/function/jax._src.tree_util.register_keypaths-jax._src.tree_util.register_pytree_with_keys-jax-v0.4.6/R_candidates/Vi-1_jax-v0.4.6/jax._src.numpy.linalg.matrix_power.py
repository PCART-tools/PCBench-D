@_wraps(np.linalg.matrix_power)
@partial(jit, static_argnames=('n',))
def matrix_power(a: ArrayLike, n: int) -> Array:
  _check_arraylike("jnp.linalg.matrix_power", a)
  arr, = _promote_dtypes_inexact(jnp.asarray(a))

  if arr.ndim < 2:
    raise TypeError("{}-dimensional array given. Array must be at least "
                    "two-dimensional".format(arr.ndim))
  if arr.shape[-2] != arr.shape[-1]:
    raise TypeError("Last 2 dimensions of the array must be square")
  try:
    n = operator.index(n)
  except TypeError as err:
    raise TypeError(f"exponent must be an integer, got {n}") from err

  if n == 0:
    return jnp.broadcast_to(jnp.eye(arr.shape[-2], dtype=arr.dtype), arr.shape)
  elif n < 0:
    arr = inv(arr)
    n = abs(n)

  if n == 1:
    return arr
  elif n == 2:
    return arr @ arr
  elif n == 3:
    return (arr @ arr) @ arr

  z = result = None
  while n > 0:
    z = arr if z is None else (z @ z)  # type: ignore[operator]
    n, bit = divmod(n, 2)
    if bit:
      result = z if result is None else (result @ z)
  assert result is not None
  return result
