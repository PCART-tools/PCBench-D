@partial(api.jit, inline=True)
def _broadcast_arrays(*args):
  """Like Numpy's broadcast_arrays but doesn't return views."""
  shapes = [np.shape(arg) for arg in args]
  if not shapes or all(core.symbolic_equal_shape(shapes[0], s) for s in shapes):
    # TODO(mattjj): remove the array(arg) here
    return [arg if isinstance(arg, ndarray) or np.isscalar(arg) else _asarray(arg)
            for arg in args]
  result_shape = lax.broadcast_shapes(*shapes)
  return [_broadcast_to(arg, result_shape) for arg in args]
