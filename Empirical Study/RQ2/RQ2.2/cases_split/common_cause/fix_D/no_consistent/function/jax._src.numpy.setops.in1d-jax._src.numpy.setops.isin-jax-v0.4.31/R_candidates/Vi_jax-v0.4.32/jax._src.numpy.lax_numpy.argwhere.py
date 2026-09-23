def argwhere(
    a: ArrayLike,
    *,
    size: int | None = None,
    fill_value: ArrayLike | None = None,
) -> Array:
  """Find the indices of nonzero array elements

  JAX implementation of :func:`numpy.argwhere`.

  ``jnp.argwhere(x)`` is essentially equivalent to ``jnp.column_stack(jnp.nonzero(x))``
  with special handling for zero-dimensional (i.e. scalar) inputs.

  Because the size of the output of ``argwhere`` is data-dependent, the function is not
  typically compatible with JIT. The JAX version adds the optional ``size`` argument, which
  specifies the size of the leading dimension of the output - it must be specified statically
  for ``jnp.argwhere`` to be compiled with non-static operands. See :func:`jax.numpy.nonzero`
  for a full discussion of ``size`` and its semantics.

  Args:
    a: array for which to find nonzero elements
    size: optional integer specifying statically the number of expected nonzero elements.
      This must be specified in order to use ``argwhere`` within JAX transformations like
      :func:`jax.jit`. See :func:`jax.numpy.nonzero` for more information.
    fill_value: optional array specifying the fill value when ``size`` is specified.
      See :func:`jax.numpy.nonzero` for more information.

  Returns:
    a two-dimensional array of shape ``[size, x.ndim]``. If ``size`` is not specified as
    an argument, it is equal to the number of nonzero elements in ``x``.

  See Also:
    - :func:`jax.numpy.where`
    - :func:`jax.numpy.nonzero`

  Examples:
    Two-dimensional array:

    >>> x = jnp.array([[1, 0, 2],
    ...                [0, 3, 0]])
    >>> jnp.argwhere(x)
    Array([[0, 0],
           [0, 2],
           [1, 1]], dtype=int32)

    Equivalent computation using :func:`jax.numpy.column_stack` and :func:`jax.numpy.nonzero`:

    >>> jnp.column_stack(jnp.nonzero(x))
    Array([[0, 0],
           [0, 2],
           [1, 1]], dtype=int32)

    Special case for zero-dimensional (i.e. scalar) inputs:

    >>> jnp.argwhere(1)
    Array([], shape=(1, 0), dtype=int32)
    >>> jnp.argwhere(0)
    Array([], shape=(0, 0), dtype=int32)
  """
  result = transpose(vstack(nonzero(atleast_1d(a), size=size, fill_value=fill_value)))
  if ndim(a) == 0:
    return result[:0].reshape(result.shape[0], 0)
  return result.reshape(result.shape[0], ndim(a))
