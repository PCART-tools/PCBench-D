@_wraps(np.linalg.matrix_power)
@partial(jit, static_argnames=('n',))
def matrix_power(a, n):
  a, = _promote_dtypes_inexact(jnp.asarray(a))

  if a.ndim < 2:
    raise TypeError("{}-dimensional array given. Array must be at least "
                    "two-dimensional".format(a.ndim))
  if a.shape[-2] != a.shape[-1]:
    raise TypeError("Last 2 dimensions of the array must be square")
  try:
    n = operator.index(n)
  except TypeError as err:
    raise TypeError(f"exponent must be an integer, got {n}") from err

  if n == 0:
    return jnp.broadcast_to(jnp.eye(a.shape[-2], dtype=a.dtype), a.shape)
  elif n < 0:
    a = inv(a)
    n = np.abs(n)

  if n == 1:
    return a
  elif n == 2:
    return a @ a
  elif n == 3:
    return (a @ a) @ a

  z = result = None
  while n > 0:
    z = a if z is None else (z @ z)
    n, bit = divmod(n, 2)
    if bit:
      result = z if result is None else (result @ z)

  return result
