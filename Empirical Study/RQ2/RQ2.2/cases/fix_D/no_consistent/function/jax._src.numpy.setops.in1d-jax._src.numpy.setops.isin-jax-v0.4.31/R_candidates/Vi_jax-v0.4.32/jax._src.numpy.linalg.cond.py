@partial(jit, static_argnames=['p'])
def cond(x: ArrayLike, p=None):
  """Compute the condition number of a matrix.

  JAX implementation of :func:`numpy.linalg.cond`.

  The condition number is defined as ``norm(x, p) * norm(inv(x), p)``. For ``p = 2``
  (the default), the condition number is the ratio of the largest to the smallest
  singular value.

  Args:
    x: array of shape ``(..., M, N)`` for which to compute the condition number.
    p: the order of the norm to use. One of ``{None, 1, -1, 2, -2, inf, -inf, 'fro'}``;
      see :func:`jax.numpy.linalg.norm` for the meaning of these. The default is ``p = None``,
      which is equivalent to ``p = 2``. If not in ``{None, 2, -2}`` then ``x`` must be square,
      i.e. ``M = N``.

  Returns:
    array of shape ``x.shape[:-2]`` containing the condition number.

  See also:
    :func:`jax.numpy.linalg.norm`

  Examples:

    Well-conditioned matrix:

    >>> x = jnp.array([[1, 2],
    ...                [2, 1]])
    >>> jnp.linalg.cond(x)
    Array(3., dtype=float32)

    Ill-conditioned matrix:

    >>> x = jnp.array([[1, 2],
    ...                [0, 0]])
    >>> jnp.linalg.cond(x)
    Array(inf, dtype=float32)
  """
  check_arraylike("cond", x)
  arr = jnp.asarray(x)
  if arr.ndim < 2:
    raise ValueError(f"jnp.linalg.cond: input array must be at least 2D; got {arr.shape=}")
  if arr.shape[-1] == 0 or arr.shape[-2] == 0:
    raise ValueError(f"jnp.linalg.cond: input array must not be empty; got {arr.shape=}")
  if p is None or p == 2:
    s = svdvals(x)
    return s[..., 0] / s[..., -1]
  elif p == -2:
    s = svdvals(x)
    r = s[..., -1] / s[..., 0]
  else:
    if arr.shape[-2] != arr.shape[-1]:
      raise ValueError(f"jnp.linalg.cond: for {p=}, array must be square; got {arr.shape=}")
    r = norm(x, ord=p, axis=(-2, -1)) * norm(inv(x), ord=p, axis=(-2, -1))
  # Convert NaNs to infs where original array has no NaNs.
  return jnp.where(ufuncs.isnan(r) & ~ufuncs.isnan(x).any(axis=(-2, -1)), jnp.inf, r)
