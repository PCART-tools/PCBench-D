@partial(jit, static_argnames=('axis', 'keepdims'), inline=True)
def _argmax(a, axis: Optional[int] = None, out=None, keepdims=False):
  _check_arraylike("argmax", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.argmax is not supported.")
  if axis is None:
    dims = list(range(ndim(a)))
    a = ravel(a)
    axis = 0
  else:
    dims = [axis]
  if a.shape[axis] == 0:
    raise ValueError("attempt to get argmax of an empty sequence")
  result = lax.argmax(a, _canonicalize_axis(axis, a.ndim), dtypes.canonicalize_dtype(int_))
  return expand_dims(result, dims) if keepdims else result
