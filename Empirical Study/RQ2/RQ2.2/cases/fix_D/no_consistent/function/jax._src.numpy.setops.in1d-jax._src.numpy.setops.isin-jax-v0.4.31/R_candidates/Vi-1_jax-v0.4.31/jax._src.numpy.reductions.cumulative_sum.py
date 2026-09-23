@implements(getattr(np, 'cumulative_sum', None))
def cumulative_sum(
    x: ArrayLike, /, *, axis: int | None = None,
    dtype: DTypeLike | None = None,
    include_initial: bool = False) -> Array:
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
