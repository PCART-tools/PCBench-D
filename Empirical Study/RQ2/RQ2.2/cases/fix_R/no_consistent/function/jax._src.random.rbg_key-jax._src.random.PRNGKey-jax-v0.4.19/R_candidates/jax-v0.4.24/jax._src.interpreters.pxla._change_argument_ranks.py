@lu.transformation
def _change_argument_ranks(in_axes, out_axes_thunk, *args):
  args = tuple(
      arg if in_axis is None else jax.lax.squeeze(arg, dimensions=(in_axis,))
      for in_axis, arg in zip(in_axes, args)
  )
  results = yield (args, {})
  out_axes = out_axes_thunk()
  yield tuple(
      x if axis is None else jax.lax.expand_dims(x, dimensions=(axis,))
      for x, axis in zip(results, out_axes)
  )
