@util.implements(getattr(np, "concat", None))
def concat(arrays: Sequence[ArrayLike], /, *, axis: int | None = 0) -> Array:
  util.check_arraylike("concat", *arrays)
  return jax.numpy.concatenate(arrays, axis=axis)
