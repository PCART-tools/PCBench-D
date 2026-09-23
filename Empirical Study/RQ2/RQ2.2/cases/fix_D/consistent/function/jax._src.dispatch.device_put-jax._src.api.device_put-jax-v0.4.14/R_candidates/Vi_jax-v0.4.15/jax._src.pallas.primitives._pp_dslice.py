def _pp_dslice(dim: int, slice: Slice, context):
  size = pp.text(str(slice.size))
  if isinstance(slice.start, int):
    if slice.start == 0:
      start = pp.text("")
    else:
      start = pp.text(str(slice.start))
    if slice.size == dim:
      end = pp.text("")
    else:
      end = pp.text(str(slice.start + slice.size))
  else:
    start = pp.text(jax_core.pp_var(slice.start, context))
    end = pp.concat([start, pp.text("+"), size])
  return pp.concat([start, pp.text(":"), end])
