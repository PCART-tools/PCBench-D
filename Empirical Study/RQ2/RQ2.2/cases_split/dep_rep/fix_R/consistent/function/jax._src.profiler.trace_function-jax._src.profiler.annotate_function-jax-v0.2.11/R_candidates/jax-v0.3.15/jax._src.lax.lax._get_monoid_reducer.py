def _get_monoid_reducer(monoid_op: Callable,
                        xs: Sequence[Array]) -> Optional[Callable]:
  if len(xs) != 1:
    return None
  x, = xs
  aval = core.get_aval(x)
  dtype = _dtype(x)
  if (type(aval) is ConcreteArray) and aval.shape == ():
    if monoid_op is add:
      return np.equal(aval.val, 0) and partial(_reduce_sum)
    elif monoid_op is mul:
      return np.equal(aval.val, 1) and _reduce_prod
    elif monoid_op is bitwise_or and dtype == np.bool_:
      return np.equal(aval.val, _get_max_identity(dtype)) and _reduce_or
    elif monoid_op is bitwise_and and dtype == np.bool_:
      return np.equal(aval.val, _get_min_identity(dtype)) and _reduce_and
    elif monoid_op is bitwise_xor and dtype == np.bool_:
      return np.equal(aval.val, _get_max_identity(dtype)) and _reduce_xor
    elif monoid_op is max:
      return np.equal(aval.val, _get_max_identity(dtype)) and _reduce_max
    elif monoid_op is min:
      return np.equal(aval.val, _get_min_identity(dtype)) and _reduce_min
  return None
