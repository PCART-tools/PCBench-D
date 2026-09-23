@partial(api.jit, static_argnames=('axis', 'dtype'))
def nancumprod(a: ArrayLike, axis: int | None = None,
               dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative product of elements along an axis, ignoring NaN values.

  JAX implementation of :func:`numpy.nancumprod`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated product along the given axis.

  See also:
    - :func:`jax.numpy.cumprod`: cumulative product without ignoring NaN values.
    - :meth:`jax.numpy.multiply.accumulate`: cumulative product via ufunc methods.
    - :func:`jax.numpy.prod`: product along axis

  Examples:
    >>> x = jnp.array([[1., 2., jnp.nan],
    ...                [4., jnp.nan, 6.]])

    The standard cumulative product will propagate NaN values:

    >>> jnp.cumprod(x)
    Array([ 1.,  2., nan, nan, nan, nan], dtype=float32)

    :func:`~jax.numpy.nancumprod` will ignore NaN values, effectively replacing
    them with ones:

    >>> jnp.nancumprod(x)
    Array([ 1.,  2.,  2.,  8.,  8., 48.], dtype=float32)

    Cumulative product along axis 1:

    >>> jnp.nancumprod(x, axis=1)
    Array([[ 1.,  2.,  2.],
           [ 4.,  4., 24.]], dtype=float32)
  """
  return _cumulative_reduction("nancumprod", lax.cumprod, a, axis, dtype, out,
                               fill_nan=True, fill_value=1)
