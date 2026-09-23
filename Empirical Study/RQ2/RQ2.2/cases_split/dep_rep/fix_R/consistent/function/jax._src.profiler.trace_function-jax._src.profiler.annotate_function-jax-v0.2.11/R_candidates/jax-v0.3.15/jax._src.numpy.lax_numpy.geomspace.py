@_wraps(np.geomspace)
def geomspace(start, stop, num=50, endpoint=True, dtype=None, axis: int = 0):
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.geomspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.geomspace")
  return _geomspace(start, stop, num, endpoint, dtype, axis)
