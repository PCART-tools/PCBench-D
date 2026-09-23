def cumulative_sum(
    x: ArrayLike, /, *, axis: int | None = None,
    dtype: DTypeLike | None = None,
    include_initial: bool = False) -> Array:
  """Cumulative sum along the axis of an array.

  JAX implementation of :func:`numpy.cumulative_sum`.

  Args:
    x: N-dimensional array
    axis: integer axis along which to accumulate. If ``x`` is one-dimensional,
      this argument is optional.
    dtype: optional dtype of the output.
    include_initial: if True, then include the initial value in the cumulative
      sum. Default is False.

  Returns:
    An array containing the accumulated values.

  See Also:
    - :func:`jax.numpy.cumsum`: alternative API for cumulative sum.
    - :func:`jax.numpy.nancumsum`: cumulative sum while ignoring NaN values.
    - :func:`jax.numpy.add.accumulate`: cumulative sum via the ufunc API.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumulative_sum(x, axis=1)
    Array([[ 1,  3,  6],
           [ 4,  9, 15]], dtype=int32)
    >>> jnp.cumulative_sum(x, axis=1, include_initial=True)
    Array([[ 0,  1,  3,  6],
           [ 0,  4,  9, 15]], dtype=int32)
  """
  check_arraylike("cumulative_sum", x)
  x = lax_internal.asarray(x)
  if x.ndim == 0:
    raise ValueError(
      "The input must be non-scalar to take a cumulative sum, however a "
      "scalar value or scalar array was given."
    )
  if axis is None:
    axis = 0
    if x.ndim > 1:
      raise ValueError(
        f"The input array has rank {x.ndim}, however axis was not set to an "
        "explicit value. The axis argument is only optional for one-dimensional "
        "arrays.")

  axis = _canonicalize_axis(axis, x.ndim)
  dtypes.check_user_dtype_supported(dtype)
  out = _cumsum_with_promotion(x, axis=axis, dtype=dtype)
  if include_initial:
    zeros_shape = list(x.shape)
    zeros_shape[axis] = 1
    out = lax_internal.concatenate(
      [lax_internal.full(zeros_shape, 0, dtype=out.dtype), out],
      dimension=axis)
  return out
