@util.implements(np.append)
@partial(jit, static_argnames=('axis',))
def append(
    arr: ArrayLike, values: ArrayLike, axis: int | None = None
) -> Array:
  if axis is None:
    return concatenate([ravel(arr), ravel(values)], 0)
  else:
    return concatenate([arr, values], axis=axis)
