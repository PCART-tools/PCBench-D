@util.implements(np.logspace)
def logspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, base: ArrayLike = 10.0,
             dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.logspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.logspace")
  return _logspace(start, stop, num, endpoint, base, dtype, axis)
