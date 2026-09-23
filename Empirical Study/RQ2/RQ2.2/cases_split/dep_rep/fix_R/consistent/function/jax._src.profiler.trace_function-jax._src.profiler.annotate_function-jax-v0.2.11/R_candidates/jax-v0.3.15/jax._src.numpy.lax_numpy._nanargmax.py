@partial(jit, static_argnames=('axis', 'keepdims'))
def _nanargmax(a, axis: Optional[int] = None, keepdims: bool = False):
  _check_arraylike("nanargmax", a)
  if not issubdtype(_dtype(a), inexact):
    return argmax(a, axis=axis, keepdims=keepdims)
  nan_mask = isnan(a)
  a = where(nan_mask, -inf, a)
  res = argmax(a, axis=axis, keepdims=keepdims)
  return where(all(nan_mask, axis=axis, keepdims=keepdims), -1, res)
