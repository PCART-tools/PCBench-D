def _get_monoid_window_reducer(monoid_op: Callable,
                               xs: Sequence[Array]) -> Callable | None:
  if len(xs) != 1:
    return None
  x, = xs
  aval = core.get_aval(x)
  if (type(aval) is ConcreteArray) and aval.shape == ():
    if monoid_op is lax.add:
      return aval.val == 0 and _reduce_window_sum
    elif monoid_op is lax.max:
      return (aval.val == lax._get_max_identity(aval.dtype)
              and _reduce_window_max)
    elif monoid_op is lax.min:
      return (aval.val == lax._get_min_identity(aval.dtype)
              and _reduce_window_min)
  return None
