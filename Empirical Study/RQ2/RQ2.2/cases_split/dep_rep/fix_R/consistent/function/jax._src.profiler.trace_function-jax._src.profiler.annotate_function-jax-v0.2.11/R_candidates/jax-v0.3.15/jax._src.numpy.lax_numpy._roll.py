@partial(jit, static_argnums=(2,))
def _roll(a, shift, axis):
  a_shape = shape(a)
  if axis is None:
    return lax.reshape(_roll(ravel(a), shift, axis=0), a_shape)
  shift = asarray(shift)
  a_ndim = len(a_shape)
  axis = np.asarray(axis)
  b_shape = lax.broadcast_shapes(shift.shape, axis.shape, (1,))
  if len(b_shape) != 1:
    msg = "'shift' and 'axis' arguments to roll must be scalars or 1D arrays"
    raise ValueError(msg)

  for x, i in zip(broadcast_to(shift, b_shape),
                  np.broadcast_to(axis, b_shape)):
    i = _canonicalize_axis(i, a_ndim)
    x = remainder(x, (a_shape[i] or 1))
    a = lax.concatenate((a, a), i)
    a = lax.dynamic_slice_in_dim(a, a_shape[i] - x, a_shape[i], axis=i)
  return a
