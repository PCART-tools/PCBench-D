def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1,
           precision: PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the (batched) vector conjugate dot product of two arrays.

  JAX implementation of :func:`numpy.linalg.vecdot`.

  Args:
    x1: left-hand side array.
    x2: right-hand side array. Size of ``x2[axis]`` must match size of ``x1[axis]``,
      and remaining dimensions must be broadcast-compatible.
    axis: axis along which to compute the dot product (default: -1)
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``x1`` and ``x2``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the conjugate dot product of ``x1`` and ``x2`` along ``axis``.
    The non-contracted dimensions are broadcast together.

  See also:
    - :func:`jax.numpy.vecdot`: similar API in the ``jax.numpy`` namespace.
    - :func:`jax.numpy.linalg.matmul`: matrix multiplication.
    - :func:`jax.numpy.linalg.tensordot`: general tensor dot product.

  Examples:
    Vector dot product of two 1D arrays:

    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.vecdot(x1, x2)
    Array(32, dtype=int32)

    Batched vector dot product of two 2D arrays:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> x2 = jnp.array([[2, 3, 4]])
    >>> jnp.linalg.vecdot(x1, x2, axis=-1)
    Array([20, 47], dtype=int32)
  """
  check_arraylike('jnp.linalg.vecdot', x1, x2)
  return jnp.vecdot(x1, x2, axis=axis, precision=precision,
                    preferred_element_type=preferred_element_type)
