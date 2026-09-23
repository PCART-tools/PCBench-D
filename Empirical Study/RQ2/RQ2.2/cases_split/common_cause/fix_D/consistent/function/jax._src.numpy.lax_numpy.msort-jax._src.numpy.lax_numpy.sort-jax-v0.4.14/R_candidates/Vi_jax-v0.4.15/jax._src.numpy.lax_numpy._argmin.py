@partial(jit, static_argnames=('axis', 'keepdims'), inline=True)
def _argmin(a: Array, axis: int | None = None, keepdims: bool = False) -> Array:
  if axis is None:
    dims = list(range(ndim(a)))
    a = ravel(a)
    axis = 0
  else:
    dims = [axis]
  if a.shape[axis] == 0:
    raise ValueError("attempt to get argmin of an empty sequence")
  result = lax.argmin(a, _canonicalize_axis(axis, a.ndim), dtypes.canonicalize_dtype(int_))
  return expand_dims(result, dims) if keepdims else result
