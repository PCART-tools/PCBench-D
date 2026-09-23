def _matchaxis_symbolic_zeros(axis_name, sz, name, src, dst, x, sum_match=False):
  # Just like `matchaxis`, but handles symbolic zeros using ad_util.py
  # TODO(mattjj): dedup with matchaxis
  if isinstance(x, (Zero, SymbolicZero)):
    if src == dst:
      return x
    elif type(src) == type(dst) == int:
      aval = core.mapped_aval(sz, src, x.aval)
      return Zero(core.unmapped_aval(sz, name, dst, aval))
    elif src is not_mapped and dst is not not_mapped:
      return Zero(core.unmapped_aval(sz, name, dst, x.aval))
    elif dst is not_mapped and sum_match:
      return Zero(core.mapped_aval(sz, src, x.aval))
    else:
      raise ValueError((axis_name, x, src, dst))
  else:
    return matchaxis(axis_name, sz, src, dst, x, sum_match=sum_match)
