@_wraps(np.logspace)
def logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None,
             axis: int = 0):
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.logspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.logspace")
  return _logspace(start, stop, num, endpoint, base, dtype, axis)
