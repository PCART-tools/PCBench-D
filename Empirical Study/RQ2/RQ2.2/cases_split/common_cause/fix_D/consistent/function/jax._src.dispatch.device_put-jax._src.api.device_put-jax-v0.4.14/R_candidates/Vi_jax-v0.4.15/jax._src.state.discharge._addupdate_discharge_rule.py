@register_discharge_rule(addupdate_p)
def _addupdate_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, val, *non_slice_idx,
    indexed_dims: Sequence[bool]):
  del in_avals, out_avals
  ans = _addupdate_discharge(x, val, non_slice_idx, indexed_dims)
  return (ans, None) + (None,) * len(non_slice_idx), []
