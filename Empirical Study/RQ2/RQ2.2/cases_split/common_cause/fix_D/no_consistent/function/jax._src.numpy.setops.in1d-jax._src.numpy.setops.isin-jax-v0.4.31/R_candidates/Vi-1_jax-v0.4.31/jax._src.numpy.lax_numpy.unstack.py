@util.implements(getattr(np, 'unstack', None))
@partial(jit, static_argnames="axis")
def unstack(x: ArrayLike, /, *, axis: int = 0) -> tuple[Array, ...]:
  util.check_arraylike("unstack", x)
  x = asarray(x)
  if x.ndim == 0:
    raise ValueError(
      "Unstack requires arrays with rank > 0, however a scalar array was "
      "passed."
    )
  return tuple(moveaxis(x, axis, 0))
