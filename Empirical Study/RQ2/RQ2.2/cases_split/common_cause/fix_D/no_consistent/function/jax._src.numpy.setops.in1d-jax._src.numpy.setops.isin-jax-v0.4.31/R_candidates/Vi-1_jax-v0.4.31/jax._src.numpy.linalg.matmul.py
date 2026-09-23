def matmul(x1: ArrayLike, x2: ArrayLike, /, *,
           precision: PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Perform a matrix multiplication.

  JAX implementation of :func:`numpy.linalg.matmul`.

  Args:
    x1: first input array, of shape ``(..., N)``.
    x2: second input array. Must have shape ``(N,)`` or ``(..., N, M)``.
      In the multi-dimensional case, leading dimensions must be broadcast-compatible
      with the leading dimensions of ``x1``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``x1`` and ``x2``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the matrix product of the inputs. Shape is ``x1.shape[:-1]``
    if ``x2.ndim == 1``, otherwise the shape is ``(..., M)``.

  See Also:
    :func:`jax.numpy.matmul`: NumPy API for this function.
    :func:`jax.numpy.linalg.vecdot`: batched vector product.
    :func:`jax.numpy.linalg.tensordot`: batched tensor product.

  Examples:
    Vector dot products:

    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.matmul(x1, x2)
    Array(32, dtype=int32)

    Matrix dot product:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> x2 = jnp.array([[1, 2],
    ...                 [3, 4],
    ...                 [5, 6]])
    >>> jnp.linalg.matmul(x1, x2)
    Array([[22, 28],
           [49, 64]], dtype=int32)

    For convenience, in all cases you can do the same computation using
    the ``@`` operator:

    >>> x1 @ x2
    Array([[22, 28],
           [49, 64]], dtype=int32)
  """
  check_arraylike('jnp.linalg.matmul', x1, x2)
  return jnp.matmul(x1, x2, precision=precision,
                    preferred_element_type=preferred_element_type)
