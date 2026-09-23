def slice(operand: ArrayLike, start_indices: Sequence[int],
          limit_indices: Sequence[int],
          strides: Optional[Sequence[int]] = None) -> Array:
  """Wraps XLA's `Slice
  <https://www.tensorflow.org/xla/operation_semantics#slice>`_
  operator.

  Args:
    operand: an array to slice
    start_indices: a sequence of ``operand.ndim`` start indices.
    limit_indices: a sequence of ``operand.ndim`` limit indices.
    strides: an optional sequence of ``operand.ndim`` strides.

  Returns:
    The sliced array

  Examples:
    Here are some examples of simple two-dimensional slices:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> lax.slice(x, (1, 0), (3, 2))
    Array([[4, 5],
           [8, 9]], dtype=int32)

    >>> lax.slice(x, (0, 0), (3, 4), (1, 2))
    Array([[ 0,  2],
           [ 4,  6],
           [ 8, 10]], dtype=int32)

    These two examples are equivalent to the following Python slicing syntax:

    >>> x[1:3, 0:2]
    Array([[4, 5],
           [8, 9]], dtype=int32)

    >>> x[0:3, 0:4:2]
    Array([[ 0,  2],
           [ 4,  6],
           [ 8, 10]], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice_in_dim`
    - :func:`jax.lax.index_in_dim`
    - :func:`jax.lax.dynamic_slice`
  """
  return slice_p.bind(operand, start_indices=tuple(start_indices),
                      limit_indices=tuple(limit_indices),
                      strides=None if strides is None else tuple(strides))
