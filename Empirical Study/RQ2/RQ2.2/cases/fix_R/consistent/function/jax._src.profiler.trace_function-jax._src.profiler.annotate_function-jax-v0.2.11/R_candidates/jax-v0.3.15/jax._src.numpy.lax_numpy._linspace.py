@partial(jit, static_argnames=('num', 'endpoint', 'retstep', 'dtype', 'axis'))
def _linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
              axis: int = 0):
  """Implementation of linspace differentiable in start and stop args."""
  lax_internal._check_user_dtype_supported(dtype, "linspace")
  if num < 0:
    raise ValueError(f"Number of samples, {num}, must be non-negative.")
  _check_arraylike("linspace", start, stop)

  if dtype is None:
    dtype = dtypes._to_inexact_dtype(result_type(start, stop))
  dtype = _jnp_dtype(dtype)
  computation_dtype = dtypes._to_inexact_dtype(dtype)
  start = asarray(start, dtype=computation_dtype)
  stop = asarray(stop, dtype=computation_dtype)

  bounds_shape = list(lax.broadcast_shapes(shape(start), shape(stop)))
  broadcast_start = broadcast_to(start, bounds_shape)
  broadcast_stop = broadcast_to(stop, bounds_shape)
  axis = len(bounds_shape) + axis + 1 if axis < 0 else axis
  bounds_shape.insert(axis, 1)
  div = (num - 1) if endpoint else num
  if num > 1:
    delta = lax.convert_element_type(stop - start, computation_dtype) / div
    iota_shape = [1,] * len(bounds_shape)
    iota_shape[axis] = div
    # This approach recovers the endpoints with float32 arithmetic,
    # but can lead to rounding errors for integer outputs.
    real_dtype = finfo(computation_dtype).dtype
    step = reshape(lax.iota(real_dtype, div), iota_shape) / div
    step = step.astype(computation_dtype)
    out = (reshape(broadcast_start, bounds_shape) * (1 - step) +
      reshape(broadcast_stop, bounds_shape) * step)

    if endpoint:
      out = lax.concatenate([out, lax.expand_dims(broadcast_stop, (axis,))],
                            _canonicalize_axis(axis, out.ndim))

  elif num == 1:
    delta = nan if endpoint else stop - start
    out = reshape(broadcast_start, bounds_shape)
  else: # num == 0 degenerate case, match numpy behavior
    empty_shape = list(lax.broadcast_shapes(shape(start), shape(stop)))
    empty_shape.insert(axis, 0)
    delta = nan
    out = reshape(array([], dtype=dtype), empty_shape)

  if issubdtype(dtype, integer) and not issubdtype(out.dtype, integer):
    out = lax.floor(out)

  if retstep:
    return lax.convert_element_type(out, dtype), delta
  else:
    return lax.convert_element_type(out, dtype)
