def unravel_index(indices: ArrayLike, shape: Shape) -> tuple[Array, ...]:
  """Convert flat indices into multi-dimensional indices.

  JAX implementation of :func:`numpy.unravel_index`. The JAX version differs in
  its treatment of out-of-bound indices: unlike NumPy, negative indices are
  supported, and out-of-bound indices are clipped to the nearest valid value.

  Args:
    indices: integer array of flat indices
    shape: shape of multidimensional array to index into

  Returns:
    Tuple of unraveled indices

  See also:
    :func:`jax.numpy.ravel_multi_index`: Inverse of this function.

  Examples:
    Start with a 1D array values and indices:

    >>> x = jnp.array([2., 3., 4., 5., 6., 7.])
    >>> indices = jnp.array([1, 3, 5])
    >>> print(x[indices])
    [3. 5. 7.]

    Now if ``x`` is reshaped, ``unravel_indices`` can be used to convert
    the flat indices into a tuple of indices that access the same entries:

    >>> shape = (2, 3)
    >>> x_2D = x.reshape(shape)
    >>> indices_2D = jnp.unravel_index(indices, shape)
    >>> indices_2D
    (Array([0, 1, 1], dtype=int32), Array([1, 0, 2], dtype=int32))
    >>> print(x_2D[indices_2D])
    [3. 5. 7.]

    The inverse function, ``ravel_multi_index``, can be used to obtain the
    original indices:

    >>> jnp.ravel_multi_index(indices_2D, shape)
    Array([1, 3, 5], dtype=int32)
  """
  util.check_arraylike("unravel_index", indices)
  indices_arr = asarray(indices)
  # Note: we do not convert shape to an array, because it may be passed as a
  # tuple of weakly-typed values, and asarray() would strip these weak types.
  try:
    shape = list(shape)
  except TypeError:
    # TODO: Consider warning here since shape is supposed to be a sequence, so
    # this should not happen.
    shape = [shape]
  if any(ndim(s) != 0 for s in shape):
    raise ValueError("unravel_index: shape should be a scalar or 1D sequence.")
  out_indices: list[ArrayLike] = [0] * len(shape)
  for i, s in reversed(list(enumerate(shape))):
    indices_arr, out_indices[i] = ufuncs.divmod(indices_arr, s)
  oob_pos = indices_arr > 0
  oob_neg = indices_arr < -1
  return tuple(where(oob_pos, s - 1, where(oob_neg, 0, i))
               for s, i in safe_zip(shape, out_indices))
