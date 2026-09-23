def subst_axis_names_var(v: Var, subst: AxisSubst, var_map: dict[Var, Var]) -> Var:
  # Var identity is load-bearing, so we can't have duplicates!
  if isinstance(v, DropVar): return v
  assert v not in var_map
  if not hasattr(v.aval, 'named_shape'):
    var_map[v] = v
    return v
  names = tuple(it.chain.from_iterable(subst(name) for name in v.aval.named_shape))
  named_shape = {name: axis_frame(name).size for name in names}
  if len(named_shape) != len(names):
    raise DuplicateAxisNameError(v)
  new_v = Var(v.count, v.suffix, v.aval.update(named_shape=named_shape))
  var_map[v] = new_v
  return new_v
