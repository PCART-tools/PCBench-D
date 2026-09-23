@partial(jit, static_argnames=('n',))
def matrix_power(a: ArrayLike, n: int) -> Array:
  """Raise a square matrix to an integer power.

  JAX implementation of :func:`numpy.linalg.matrix_power`, implemented via
  repeated squarings.

  Args:
    a: array of shape ``(..., M, M)`` to be raised to the power `n`.
    n: the integer exponent to which the matrix should be raised.

  Returns:
    Array of shape ``(..., M, M)`` containing the matrix power of a to the n.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [3., 4.]])
    >>> jnp.linalg.matrix_power(a, 3)
    Array([[ 37.,  54.],
           [ 81., 118.]], dtype=float32)
    >>> a @ a @ a  # equivalent evaluated directly
    Array([[ 37.,  54.],
           [ 81., 118.]], dtype=float32)

    This also supports zero powers:

    >>> jnp.linalg.matrix_power(a, 0)
    Array([[1., 0.],
           [0., 1.]], dtype=float32)

    and also supports negative powers:

    >>> with jnp.printoptions(precision=3):
    ...   jnp.linalg.matrix_power(a, -2)
    Array([[ 5.5 , -2.5 ],
           [-3.75,  1.75]], dtype=float32)

    Negative powers are equivalent to matmul of the inverse:

    >>> inv_a = jnp.linalg.inv(a)
    >>> with jnp.printoptions(precision=3):
    ...   inv_a @ inv_a
    Array([[ 5.5 , -2.5 ],
           [-3.75,  1.75]], dtype=float32)
  """
  check_arraylike("jnp.linalg.matrix_power", a)
  arr, = promote_dtypes_inexact(jnp.asarray(a))

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
