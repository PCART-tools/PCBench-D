@partial(jit, static_argnames=('axis',))
def _flip(m: Array, axis: int | tuple[int, ...] | None = None) -> Array:
  if axis is None:
    return lax.rev(m, list(range(len(shape(m)))))
  axis = _ensure_index_tuple(axis)
  return lax.rev(m, [_canonicalize_axis(ax, ndim(m)) for ax in axis])
