@register_discharge_rule(swap_p)
def _swap_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, val, *non_slice_idx,
    indexed_dims: Sequence[bool]):
  del in_avals, out_avals
  if not any(indexed_dims):
    z, x_new = x, val
  z, x_new = _swap_discharge(x, val, non_slice_idx, indexed_dims)
  return (x_new, None) + (None,) * len(non_slice_idx), z
