def reshape(operand: ArrayLike, new_sizes: Shape,
            dimensions: Sequence[int] | None = None) -> Array:
  """Wraps XLA's `Reshape
  <https://www.tensorflow.org/xla/operation_semantics#reshape>`_
  operator.

  For inserting/removing dimensions of size 1, prefer using ``lax.squeeze`` /
  ``lax.expand_dims``. These preserve information about axis identity that may
  be useful for advanced transformation rules.

  Args:
    operand: array to be reshaped.
    new_sizes: sequence of integers specifying the resulting shape. The size
      of the final array must match the size of the input.
    dimensions: optional sequence of integers specifying the permutation order of
      the input shape. If specified, the length must match ``operand.shape``.

  Returns:
    out: reshaped array.

  Examples:
    Simple reshaping from one to two dimensions:

    >>> x = jnp.arange(6)
    >>> y = reshape(x, (2, 3))
    >>> y
    Array([[0, 1, 2],
                 [3, 4, 5]], dtype=int32)

    Reshaping back to one dimension:

    >>> reshape(y, (6,))
    Array([0, 1, 2, 3, 4, 5], dtype=int32)

    Reshaping to one dimension with permutation of dimensions:

    >>> reshape(y, (6,), (1, 0))
    Array([0, 3, 1, 4, 2, 5], dtype=int32)
  """
  new_sizes = canonicalize_shape(new_sizes)  # TODO
  new_sizes = tuple(new_sizes)
  same_shape = core.definitely_equal_shape(np.shape(operand), new_sizes)
  if dimensions is None:
    same_dims = True
    dims = None
  else:
    dims = api_util._ensure_index_tuple(dimensions)
    same_dims = tuple(dims) == tuple(range(np.ndim(operand)))
  if np.shape(operand) and same_shape and same_dims and isinstance(operand, Array):
    return type_cast(Array, operand)
  else:
    dyn_shape, static_new_sizes = _extract_tracers_dyn_shape(new_sizes)

    return reshape_p.bind(
      operand, *dyn_shape, new_sizes=tuple(static_new_sizes),
      dimensions=None if dims is None or same_dims else dims)
