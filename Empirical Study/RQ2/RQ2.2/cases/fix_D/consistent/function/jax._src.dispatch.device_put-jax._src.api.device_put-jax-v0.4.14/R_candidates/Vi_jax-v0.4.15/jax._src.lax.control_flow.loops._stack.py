def _stack(aval, vals):
  vals = [lax.expand_dims(x, (0,)) for x in vals]
  return lax.concatenate(vals, 0)
