@_wraps(np.linspace)
def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis: int = 0):
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.linspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.linspace")
  return _linspace(start, stop, num, endpoint, retstep, dtype, axis)
