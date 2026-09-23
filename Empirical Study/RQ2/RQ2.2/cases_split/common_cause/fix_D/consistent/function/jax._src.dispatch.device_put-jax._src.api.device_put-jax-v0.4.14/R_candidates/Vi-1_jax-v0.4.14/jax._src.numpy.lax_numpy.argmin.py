@util._wraps(np.argmin, skip_params=['out'])
def argmin(a: ArrayLike, axis: Optional[int] = None, out=None, keepdims=None) -> Array:
  util.check_arraylike("argmin", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.argmin is not supported.")
  return _argmin(asarray(a), None if axis is None else operator.index(axis),
                 keepdims=bool(keepdims))
