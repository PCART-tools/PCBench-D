@util.implements(np.geomspace)
def geomspace(start: ArrayLike, stop: ArrayLike, num: int = 50, endpoint: bool = True,
              dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.geomspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.geomspace")
  return _geomspace(start, stop, num, endpoint, dtype, axis)
