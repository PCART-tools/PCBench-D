@register_discharge_rule(swap_p)
def _swap_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, val, *idx,
    tree):
  del in_avals, out_avals
  z, x_new = _swap_discharge(x, val, idx, tree)
  return (x_new, None) + (None,) * len(idx), z
