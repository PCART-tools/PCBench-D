def def_trivial_padding(prim: Primitive) -> None:
  if prim.multiple_results:
    padding_rules[prim] = partial(_trivial_padding_rule_multi, prim)
  else:
    padding_rules[prim] = partial(_trivial_padding_rule, prim)
