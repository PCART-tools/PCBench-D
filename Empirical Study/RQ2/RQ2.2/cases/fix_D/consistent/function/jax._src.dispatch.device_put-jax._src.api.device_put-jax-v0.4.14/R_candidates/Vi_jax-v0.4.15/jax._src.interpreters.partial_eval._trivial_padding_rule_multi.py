def _trivial_padding_rule_multi(prim, _, __, *args, **params):
  return prim.bind(*args, **params)
