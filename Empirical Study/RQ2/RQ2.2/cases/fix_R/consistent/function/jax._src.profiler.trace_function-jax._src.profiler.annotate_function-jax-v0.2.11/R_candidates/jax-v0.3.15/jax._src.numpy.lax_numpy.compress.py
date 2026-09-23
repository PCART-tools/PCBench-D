@_wraps(np.compress, skip_params=['out'])
def compress(condition, a, axis: Optional[int] = None, out=None):
  _check_arraylike("compress", condition, a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.compress is not supported.")
  if ndim(condition) != 1:
    raise ValueError("condition must be a 1D array")
  condition = asarray(condition).astype(bool)
  if axis is None:
    axis = 0
    a = ravel(a)
  else:
    a = moveaxis(a, axis, 0)
  condition, extra = condition[:a.shape[0]], condition[a.shape[0]:]
  if any(extra):
    raise ValueError("condition contains entries that are out of bounds")
  a = a[:condition.shape[0]]
  return moveaxis(a[condition], 0, axis)
