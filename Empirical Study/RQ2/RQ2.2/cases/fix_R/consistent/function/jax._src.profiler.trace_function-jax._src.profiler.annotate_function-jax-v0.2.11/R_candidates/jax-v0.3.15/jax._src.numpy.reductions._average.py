@partial(api.jit, static_argnames=('axis', 'returned', 'keepdims'), inline=True)
def _average(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, weights=None,
             returned=False, keepdims=False):
  if weights is None: # Treat all weights as 1
    _check_arraylike("average", a)
    a, = _promote_dtypes_inexact(a)
    avg = mean(a, axis=axis, keepdims=keepdims)
    if axis is None:
      weights_sum = lax.full((), core.dimension_as_value(a.size), dtype=avg.dtype)
    else:
      weights_sum = lax.full_like(avg, core.dimension_as_value(a.shape[axis]), dtype=avg.dtype)
  else:
    _check_arraylike("average", a, weights)
    a, weights = _promote_dtypes_inexact(a, weights)

    a_shape = np.shape(a)
    a_ndim = len(a_shape)
    weights_shape = np.shape(weights)
    axis = None if axis is None else _canonicalize_axis(axis, a_ndim)

    if a_shape != weights_shape:
      # Make sure the dimensions work out
      if axis is None:
        raise ValueError("Axis must be specified when shapes of a and "
                         "weights differ.")
      if len(weights_shape) != 1:
        raise ValueError("1D weights expected when shapes of a and "
                         "weights differ.")
      if not core.symbolic_equal_dim(weights_shape[0], a_shape[axis]):
        raise ValueError("Length of weights not "
                         "compatible with specified axis.")

      weights = _broadcast_to(weights, (a_ndim - 1) * (1,) + weights_shape)
      weights = _moveaxis(weights, -1, axis)

    weights_sum = sum(weights, axis=axis, keepdims=keepdims)
    avg = sum(a * weights, axis=axis, keepdims=keepdims) / weights_sum

  if returned:
    if avg.shape != weights_sum.shape:
      weights_sum = _broadcast_to(weights_sum, avg.shape)
    return avg, weights_sum
  return avg
