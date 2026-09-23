def outer(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute the outer product of two 1-dimensional arrays.

  JAX implementation of :func:`numpy.linalg.outer`.

  Args:
    x1: array
    x2: array

  Returns:
    array containing the outer product of ``x1`` and ``x2``

  See also:
    :func:`jax.numpy.outer`: similar function in the main :mod:`jax.numpy` module.

  Examples:
    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.outer(x1, x2)
    Array([[ 4,  5,  6],
           [ 8, 10, 12],
           [12, 15, 18]], dtype=int32)
  """
  check_arraylike("jnp.linalg.outer", x1, x2)
  x1, x2 = jnp.asarray(x1), jnp.asarray(x2)
  if x1.ndim != 1 or x2.ndim != 1:
    raise ValueError(f"Input arrays must be one-dimensional, but they are {x1.ndim=} {x2.ndim=}")
  return x1[:, None] * x2[None, :]
