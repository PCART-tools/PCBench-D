@util._wraps(np.nanargmax, lax_description=_NANARG_DOC.format("max"), skip_params=['out'])
def nanargmax(a, axis: Optional[int] = None, out : Any = None, keepdims : Optional[bool] = None):
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanargmax is not supported.")
  return _nanargmax(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))
