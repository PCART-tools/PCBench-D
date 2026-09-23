@partial(api.jit, static_argnames=('axis', 'dtype'))
def cumsum(a: ArrayLike, axis: int | None = None,
           dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative sum of elements along an axis.

  JAX implementation of :func:`numpy.cumsum`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated sum along the given axis.

  See also:
    - :func:`jax.numpy.cumulative_sum`: cumulative sum via the array API standard.
    - :meth:`jax.numpy.add.accumulate`: cumulative sum via ufunc methods.
    - :func:`jax.numpy.nancumsum`: cumulative sum ignoring NaN values.
    - :func:`jax.numpy.sum`: sum along axis

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumsum(x)  # flattened cumulative sum
    Array([ 1,  3,  6, 10, 15, 21], dtype=int32)
    >>> jnp.cumsum(x, axis=1)  # cumulative sum along axis 1
    Array([[ 1,  3,  6],
           [ 4,  9, 15]], dtype=int32)
  """
  return _cumulative_reduction("cumsum", lax.cumsum, a, axis, dtype, out)
