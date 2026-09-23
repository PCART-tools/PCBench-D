@partial(jit, static_argnames=('axis', 'keepdims'))
def _nanargmin(a, axis: Optional[int] = None, keepdims : bool = False):
  util._check_arraylike("nanargmin", a)
  if not issubdtype(_dtype(a), inexact):
    return argmin(a, axis=axis, keepdims=keepdims)
  nan_mask = ufuncs.isnan(a)
  a = where(nan_mask, inf, a)
  res = argmin(a, axis=axis, keepdims=keepdims)
  return where(reductions.all(nan_mask, axis=axis, keepdims=keepdims), -1, res)
