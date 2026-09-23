def ravel_multi_index(multi_index: Sequence[ArrayLike], dims: Sequence[int],
                      mode: str = 'raise', order: str = 'C') -> Array:
  """Convert multi-dimensional indices into flat indices.

  JAX implementation of :func:`numpy.ravel_multi_index`

  Args:
    multi_index: sequence of integer arrays containing indices in each dimension.
    dims: sequence of integer sizes; must have ``len(dims) == len(multi_index)``
    mode: how to handle out-of bound indices. Options are

      - ``"raise"`` (default): raise a ValueError. This mode is incompatible
        with :func:`~jax.jit` or other JAX transformations.
      - ``"clip"``: clip out-of-bound indices to valid range.
      - ``"wrap"``: wrap out-of-bound indices to valid range.

    order: ``"C"`` (default) or ``"F"``, specify whether to assume C-style
      row-major order or Fortran-style column-major order.

  Returns:
    array of flattened indices

  See also:
    :func:`jax.numpy.unravel_index`: inverse of this function.

  Examples:
    Define a 2-dimensional array and a sequence of indices of even values:

    >>> x = jnp.array([[2., 3., 4.],
    ...                [5., 6., 7.]])
    >>> indices = jnp.where(x % 2 == 0)
    >>> indices
    (Array([0, 0, 1], dtype=int32), Array([0, 2, 1], dtype=int32))
    >>> x[indices]
    Array([2., 4., 6.], dtype=float32)

    Compute the flattened indices:

    >>> indices_flat = jnp.ravel_multi_index(indices, x.shape)
    >>> indices_flat
    Array([0, 2, 4], dtype=int32)

    These flattened indices can be used to extract the same values from the
    flattened ``x`` array:

    >>> x_flat = x.ravel()
    >>> x_flat
    Array([2., 3., 4., 5., 6., 7.], dtype=float32)
    >>> x_flat[indices_flat]
    Array([2., 4., 6.], dtype=float32)

    The original indices can be recovered with :func:`~jax.numpy.unravel_index`:

    >>> jnp.unravel_index(indices_flat, x.shape)
    (Array([0, 0, 1], dtype=int32), Array([0, 2, 1], dtype=int32))
  """
  assert len(multi_index) == len(dims), f"len(multi_index)={len(multi_index)} != len(dims)={len(dims)}"
  dims = tuple(core.concrete_or_error(operator.index, d, "in `dims` argument of ravel_multi_index().") for d in dims)
  util.check_arraylike("ravel_multi_index", *multi_index)
  multi_index_arr = [asarray(i) for i in multi_index]
  for index in multi_index_arr:
    if mode == 'raise':
      core.concrete_or_error(array, index,
        "The error occurred because ravel_multi_index was jit-compiled"
        " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if not issubdtype(_dtype(index), integer):
      raise TypeError("only int indices permitted")
  if mode == "raise":
    if any(reductions.any((i < 0) | (i >= d)) for i, d in zip(multi_index_arr, dims)):
      raise ValueError("invalid entry in coordinates array")
  elif mode == "clip":
    multi_index_arr = [clip(i, 0, d - 1) for i, d in zip(multi_index_arr, dims)]
  elif mode == "wrap":
    multi_index_arr = [i % d for i, d in zip(multi_index_arr, dims)]
  else:
    raise ValueError(f"invalid mode={mode!r}. Expected 'raise', 'wrap', or 'clip'")

  if order == "F":
    strides = np.cumprod((1,) + dims[:-1])
  elif order == "C":
    strides = np.cumprod((1,) + dims[1:][::-1])[::-1]
  else:
    raise ValueError(f"invalid order={order!r}. Expected 'C' or 'F'")

  result = array(0, dtype=(multi_index_arr[0].dtype if multi_index_arr
                           else dtypes.canonicalize_dtype(int_)))
  for i, s in zip(multi_index_arr, strides):
    result = result + i * int(s)
  return result
