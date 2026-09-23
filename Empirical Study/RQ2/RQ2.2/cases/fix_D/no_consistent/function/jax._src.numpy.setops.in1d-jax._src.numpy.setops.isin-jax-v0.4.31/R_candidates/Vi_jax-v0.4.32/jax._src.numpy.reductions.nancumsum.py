@partial(api.jit, static_argnames=('axis', 'dtype'))
def nancumsum(a: ArrayLike, axis: int | None = None,
              dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative sum of elements along an axis, ignoring NaN values.

  JAX implementation of :func:`numpy.nancumsum`.

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
    - :func:`jax.numpy.cumsum`: cumulative sum without ignoring NaN values.
    - :func:`jax.numpy.cumulative_sum`: cumulative sum via the array API standard.
    - :meth:`jax.numpy.add.accumulate`: cumulative sum via ufunc methods.
    - :func:`jax.numpy.sum`: sum along axis

  Examples:
    >>> x = jnp.array([[1., 2., jnp.nan],
    ...                [4., jnp.nan, 6.]])

    The standard cumulative sum will propagate NaN values:

    >>> jnp.cumsum(x)
    Array([ 1.,  3., nan, nan, nan, nan], dtype=float32)

    :func:`~jax.numpy.nancumsum` will ignore NaN values, effectively replacing
    them with zeros:

    >>> jnp.nancumsum(x)
    Array([ 1.,  3.,  3.,  7.,  7., 13.], dtype=float32)

    Cumulative sum along axis 1:

    >>> jnp.nancumsum(x, axis=1)
    Array([[ 1.,  3.,  3.],
           [ 4.,  4., 10.]], dtype=float32)
  """
  return _cumulative_reduction("nancumsum", lax.cumsum, a, axis, dtype, out,
                               fill_nan=True, fill_value=0)
