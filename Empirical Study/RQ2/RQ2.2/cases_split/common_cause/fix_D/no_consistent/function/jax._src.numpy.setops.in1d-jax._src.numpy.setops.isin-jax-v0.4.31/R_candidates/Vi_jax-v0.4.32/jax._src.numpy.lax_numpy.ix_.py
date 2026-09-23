def ix_(*args: ArrayLike) -> tuple[Array, ...]:
  """Return a multi-dimensional grid (open mesh) from N one-dimensional sequences.

  JAX implementation of :func:`numpy.ix_`.

  Args:
    *args: N one-dimensional arrays

  Returns:
    Tuple of Jax arrays forming an open mesh, each with N dimensions.

  See Also:
    - :obj:`jax.numpy.ogrid`
    - :obj:`jax.numpy.mgrid`
    - :func:`jax.numpy.meshgrid`

  Examples:
    >>> rows = jnp.array([0, 2])
    >>> cols = jnp.array([1, 3])
    >>> open_mesh = jnp.ix_(rows, cols)
    >>> open_mesh
    (Array([[0],
          [2]], dtype=int32), Array([[1, 3]], dtype=int32))
    >>> [grid.shape for grid in open_mesh]
    [(2, 1), (1, 2)]
    >>> x = jnp.array([[10, 20, 30, 40],
    ...                [50, 60, 70, 80],
    ...                [90, 100, 110, 120],
    ...                [130, 140, 150, 160]])
    >>> x[open_mesh]
    Array([[ 20,  40],
           [100, 120]], dtype=int32)
  """
  util.check_arraylike("ix", *args)
  n = len(args)
  output = []
  for i, a in enumerate(args):
    a = asarray(a)
    if len(a.shape) != 1:
      msg = "Arguments to jax.numpy.ix_ must be 1-dimensional, got shape {}"
      raise ValueError(msg.format(a.shape))
    if _dtype(a) == bool_:
      raise NotImplementedError(
        "Boolean arguments to jax.numpy.ix_ are not implemented")
    shape = [1] * n
    shape[i] = a.shape[0]
    if a.size == 0:
      # Numpy uses an integer index type for empty arrays.
      output.append(lax.full(shape, np.zeros((), np.intp)))
    else:
      output.append(lax.broadcast_in_dim(a, shape, (i,)))
  return tuple(output)
