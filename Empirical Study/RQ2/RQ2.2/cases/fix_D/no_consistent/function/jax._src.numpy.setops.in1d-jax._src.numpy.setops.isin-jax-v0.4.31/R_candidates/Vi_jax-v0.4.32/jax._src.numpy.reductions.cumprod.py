@partial(api.jit, static_argnames=('axis', 'dtype'))
def cumprod(a: ArrayLike, axis: int | None = None,
            dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative product of elements along an axis.

  JAX implementation of :func:`numpy.cumprod`.

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
    - :meth:`jax.numpy.multiply.accumulate`: cumulative product via ufunc methods.
    - :func:`jax.numpy.nancumprod`: cumulative product ignoring NaN values.
    - :func:`jax.numpy.prod`: product along axis

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumprod(x)  # flattened cumulative product
    Array([  1,   2,   6,  24, 120, 720], dtype=int32)
    >>> jnp.cumprod(x, axis=1)  # cumulative product along axis 1
    Array([[  1,   2,   6],
           [  4,  20, 120]], dtype=int32)
  """
  return _cumulative_reduction("cumprod", lax.cumprod, a, axis, dtype, out)
