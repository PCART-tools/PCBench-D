@util._wraps(np.linspace)
def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, retstep: bool = False,
             dtype: Optional[DTypeLike] = None,
             axis: int = 0) -> Union[Array, tuple[Array, Array]]:
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.linspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.linspace")
  return _linspace(start, stop, num, endpoint, retstep, dtype, axis)
