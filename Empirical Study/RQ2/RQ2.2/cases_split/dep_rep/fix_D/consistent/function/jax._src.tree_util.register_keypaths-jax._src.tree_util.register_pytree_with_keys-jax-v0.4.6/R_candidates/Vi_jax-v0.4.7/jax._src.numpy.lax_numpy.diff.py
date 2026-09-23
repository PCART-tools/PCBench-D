@util._wraps(np.diff)
@partial(jit, static_argnames=('n', 'axis'))
def diff(a: ArrayLike, n: int = 1, axis: int = -1,
         prepend: Optional[ArrayLike] = None,
         append: Optional[ArrayLike] = None) -> Array:
  util.check_arraylike("diff", a)
  arr = asarray(a)
  n = core.concrete_or_error(operator.index, n, "'n' argument of jnp.diff")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.diff")
  if n == 0:
    return arr
  if n < 0:
    raise ValueError(f"order must be non-negative but got {n}")
  if arr.ndim == 0:
    raise ValueError(f"diff requires input that is at least one dimensional; got {a}")

  nd = arr.ndim
  axis = _canonicalize_axis(axis, nd)

  combined: List[Array] = []
  if prepend is not None:
    util.check_arraylike("diff", prepend)
    if isscalar(prepend):
      shape = list(arr.shape)
      shape[axis] = 1
      prepend = broadcast_to(prepend, tuple(shape))
    combined.append(asarray(prepend))

  combined.append(arr)

  if append is not None:
    util.check_arraylike("diff", append)
    if isscalar(append):
      shape = list(arr.shape)
      shape[axis] = 1
      append = broadcast_to(append, tuple(shape))
    combined.append(asarray(append))

  if len(combined) > 1:
    arr = concatenate(combined, axis)

  slice1 = [slice(None)] * nd
  slice2 = [slice(None)] * nd
  slice1[axis] = slice(1, None)
  slice2[axis] = slice(None, -1)
  slice1_tuple = tuple(slice1)
  slice2_tuple = tuple(slice2)

  op = ufuncs.not_equal if arr.dtype == np.bool_ else ufuncs.subtract
  for _ in range(n):
    arr = op(arr[slice1_tuple], arr[slice2_tuple])

  return arr
