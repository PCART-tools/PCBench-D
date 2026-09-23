def _trivial_padding_rule(prim, _, __, *args, **params):
  return [prim.bind(*args, **params)]
