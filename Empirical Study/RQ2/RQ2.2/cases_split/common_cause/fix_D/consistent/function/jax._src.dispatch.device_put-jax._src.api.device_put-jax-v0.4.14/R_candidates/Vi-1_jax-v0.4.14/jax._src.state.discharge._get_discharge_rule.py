@register_discharge_rule(get_p)
def _get_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, *non_slice_idx,
    indexed_dims: Sequence[bool]):
  del in_avals, out_avals
  y = _get_discharge(x, non_slice_idx, indexed_dims)
  return (None,) * (len(non_slice_idx) + 1), y
