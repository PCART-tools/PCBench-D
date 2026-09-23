def _masking_defreducer(prim, identity):
  masking.masking_rules[prim] = partial(_reducer_masking_rule, prim, identity)
