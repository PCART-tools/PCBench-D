def vector_norm(x: ArrayLike, /, *, axis: int | None = None, keepdims: bool = False,
                ord: int | str = 2) -> Array:
  """Compute the vector norm of a vector or batch of vectors.

  JAX implementation of :func:`numpy.linalg.vector_norm`.

  Args:
    x: N-dimensional array for which to take the norm.
    axis: optional axis along which to compute the vector norm. If None (default)
      then ``x`` is flattened and the norm is taken over all values.
    keepdims: if True, keep the reduced dimensions in the output.
    ord: A string or int specifying the type of norm; default is the 2-norm.
      See :func:`numpy.linalg.norm` for details on available options.

  Returns:
    array containing the norm of ``x``.

  See also:
    - :func:`jax.numpy.linalg.matrix_norm`: Norm of a matrix or stack of matrices.
    - :func:`jax.numpy.linalg.norm`: More general matrix or vector norm.

  Examples:
    Norm of a single vector:

    >>> x = jnp.array([1., 2., 3.])
    >>> jnp.linalg.vector_norm(x)
    Array(3.7416575, dtype=float32)

    Norm of a batch of vectors:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [4., 5., 7.]])
    >>> jnp.linalg.vector_norm(x, axis=1)
    Array([3.7416575, 9.486833 ], dtype=float32)
  """
  check_arraylike('jnp.linalg.vector_norm', x)
  if axis is None:
    result = norm(jnp.ravel(x), ord=ord)
    if keepdims:
      result = lax.expand_dims(result, range(jnp.ndim(x)))
    return result
  return norm(x, axis=axis, keepdims=keepdims, ord=ord)
