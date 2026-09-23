@_wraps(np.diff)
@partial(jit, static_argnames=('n', 'axis'))
def diff(a, n=1, axis: int = -1, prepend=None, append=None):
  _check_arraylike("diff", a)
  n = core.concrete_or_error(operator.index, n, "'n' argument of jnp.diff")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.diff")
  if n == 0:
    return a
  if n < 0:
    raise ValueError(f"order must be non-negative but got {n}")
  if ndim(a) == 0:
    raise ValueError(f"diff requires input that is at least one dimensional; got {a}")

  nd = a.ndim
  axis = _canonicalize_axis(axis, nd)

  combined = []
  if prepend is not None:
    _check_arraylike("diff", prepend)
    if isscalar(prepend):
      shape = list(a.shape)
      shape[axis] = 1
      prepend = broadcast_to(prepend, tuple(shape))
    combined.append(prepend)

  combined.append(a)

  if append is not None:
    _check_arraylike("diff", append)
    if isscalar(append):
      shape = list(a.shape)
      shape[axis] = 1
      append = broadcast_to(append, tuple(shape))
    combined.append(append)

  if len(combined) > 1:
    a = concatenate(combined, axis)

  slice1 = [slice(None)] * nd
  slice2 = [slice(None)] * nd
  slice1[axis] = slice(1, None)
  slice2[axis] = slice(None, -1)
  slice1_tuple = tuple(slice1)
  slice2_tuple = tuple(slice2)

  op = not_equal if a.dtype == np.bool_ else subtract
  for _ in range(n):
    a = op(a[slice1_tuple], a[slice2_tuple])

  return a
