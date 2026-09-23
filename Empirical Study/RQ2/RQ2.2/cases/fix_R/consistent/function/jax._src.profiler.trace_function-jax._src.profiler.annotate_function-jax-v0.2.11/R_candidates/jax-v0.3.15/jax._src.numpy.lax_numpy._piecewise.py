@partial(jit, static_argnames=['funcs'])
def _piecewise(x, condlist, consts, funcs, *args, **kw):
  funcs = dict(funcs)
  funclist = [consts.get(i, funcs.get(i)) for i in range(len(condlist) + 1)]
  indices = argmax(cumsum(concatenate([zeros_like(condlist[:1]), condlist], 0), 0), 0)
  dtype = _dtype(x)
  def _call(f):
    return lambda x: f(x, *args, **kw).astype(dtype)
  def _const(v):
    return lambda x: array(v, dtype=dtype)
  funclist = [_call(f) if callable(f) else _const(f) for f in funclist]
  return vectorize(lax.switch, excluded=(1,))(indices, funclist, x)
