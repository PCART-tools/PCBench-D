def _get_monoid_reducer(monoid_op: Callable,
                        xs: Sequence[Array]) -> Callable | None:
  if len(xs) != 1:
    return None
  x, = xs
  aval = core.get_aval(x)
  dtype = _dtype(x)
  if (type(aval) is ConcreteArray) and aval.shape == ():
    # allow bitwise reductions for boolean and integer types
    _is_intlike = dtype == np.bool_ or dtypes.issubdtype(dtype, np.integer)
    if monoid_op is add:
      return _reduce_sum if np.equal(aval.val, 0) else None
    elif monoid_op is mul:
      return _reduce_prod if np.equal(aval.val, 1) else None
    elif monoid_op is bitwise_or and _is_intlike:
      return _reduce_or if np.equal(aval.val, _get_bitwise_or_identity(dtype)) else None
    elif monoid_op is bitwise_and and _is_intlike:
      return _reduce_and if np.equal(aval.val, _get_bitwise_and_identity(dtype)) else None
    elif monoid_op is bitwise_xor and _is_intlike:
      return _reduce_xor if np.equal(aval.val, _get_bitwise_or_identity(dtype)) else None
    elif monoid_op is max:
      return _reduce_max if np.equal(aval.val, _get_max_identity(dtype)) else None
    elif monoid_op is min:
      return _reduce_min if np.equal(aval.val, _get_min_identity(dtype)) else None
  return None
