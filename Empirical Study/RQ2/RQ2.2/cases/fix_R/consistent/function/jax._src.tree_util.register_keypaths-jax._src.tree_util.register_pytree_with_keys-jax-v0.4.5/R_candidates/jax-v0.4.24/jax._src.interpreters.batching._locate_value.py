def _locate_value(key, in_vals, out_vals):
  for ix, candidate in enumerate(in_vals):
    if key == id(candidate):
      return pe.InDBIdx(ix)
  for ix, candidate in enumerate(out_vals):
    if key == id(candidate):
      return pe.OutDBIdx(ix)
  assert False, "Could not find segment lengths"
