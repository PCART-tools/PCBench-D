def _substitute_axis_sizes_in_aval(
    env: Dict[core.Var, ir.Value], a: core.AbstractValue) -> core.AbstractValue:
  if isinstance(a, core.DShapedArray):
    return a.update(shape=tuple(env.get(d, d) for d in a.shape))  # type: ignore
  return a
