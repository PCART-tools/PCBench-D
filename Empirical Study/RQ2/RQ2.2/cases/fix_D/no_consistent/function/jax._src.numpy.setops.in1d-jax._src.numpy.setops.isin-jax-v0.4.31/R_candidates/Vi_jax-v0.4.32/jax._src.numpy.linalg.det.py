@jit
def det(a: ArrayLike) -> Array:
  """
  Compute the determinant of an array.

  JAX implementation of :func:`numpy.linalg.det`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the determinant.

  Returns:
    An array of determinants of shape ``a.shape[:-2]``.

  See also:
    :func:`jax.scipy.linalg.det`: Scipy-style API for determinant.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.linalg.det(a)
    Array(-2., dtype=float32)
  """
  check_arraylike("jnp.linalg.det", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  a_shape = jnp.shape(a)
  if len(a_shape) >= 2 and a_shape[-1] == 2 and a_shape[-2] == 2:
    return _det_2x2(a)
  elif len(a_shape) >= 2 and a_shape[-1] == 3 and a_shape[-2] == 3:
    return _det_3x3(a)
  elif len(a_shape) >= 2 and a_shape[-1] == a_shape[-2]:
    return _det(a)
  else:
    msg = "Argument to _det() must have shape [..., n, n], got {}"
    raise ValueError(msg.format(a_shape))
