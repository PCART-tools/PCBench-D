@util._wraps(np.argmax, skip_params=['out'])
def argmax(a: ArrayLike, axis: Optional[int] = None, out=None, keepdims=None) -> Array:
  util.check_arraylike("argmax", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.argmax is not supported.")
  return _argmax(asarray(a), None if axis is None else operator.index(axis),
                 keepdims=bool(keepdims))
