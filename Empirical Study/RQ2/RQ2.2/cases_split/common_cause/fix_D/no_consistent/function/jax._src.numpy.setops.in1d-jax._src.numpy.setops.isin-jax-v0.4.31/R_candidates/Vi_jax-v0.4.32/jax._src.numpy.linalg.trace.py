def trace(x: ArrayLike, /, *,
          offset: int = 0, dtype: DTypeLike | None = None) -> Array:
  """Compute the trace of a matrix.

  JAX implementation of :func:`numpy.linalg.trace`.

  Args:
    x: array of shape ``(..., M, N)`` and whose innermost two
      dimensions form MxN matrices for which to take the trace.
    offset: positive or negative offset from the main diagonal
      (default: 0).
    dtype: data type of the returned array (default: ``None``). If ``None``,
      then output dtype will match the dtype of ``x``, promoted to default
      precision in the case of integer types.

  Returns:
    array of batched traces with shape ``x.shape[:-2]``

  See also:
    - :func:`jax.numpy.trace`: similar API in the ``jax.numpy`` namespace.

  Examples:
    Trace of a single matrix:

    >>> x = jnp.array([[1,  2,  3,  4],
    ...                [5,  6,  7,  8],
    ...                [9, 10, 11, 12]])
    >>> jnp.linalg.trace(x)
    Array(18, dtype=int32)
    >>> jnp.linalg.trace(x, offset=1)
    Array(21, dtype=int32)
    >>> jnp.linalg.trace(x, offset=-1, dtype="float32")
    Array(15., dtype=float32)

    Batched traces:

    >>> x = jnp.arange(24).reshape(2, 3, 4)
    >>> jnp.linalg.trace(x)
    Array([15, 51], dtype=int32)
  """
  check_arraylike('jnp.linalg.trace', x)
  return jnp.trace(x, offset=offset, axis1=-2, axis2=-1, dtype=dtype)
