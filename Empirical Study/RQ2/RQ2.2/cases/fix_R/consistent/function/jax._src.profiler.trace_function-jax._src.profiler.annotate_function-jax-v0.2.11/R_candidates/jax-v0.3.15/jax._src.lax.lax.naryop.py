def naryop(result_dtype, accepted_dtypes, name):
  dtype_rule = partial(naryop_dtype_rule, result_dtype, accepted_dtypes, name)
  shape_rule = partial(_broadcasting_shape_rule, name)
  weak_type_rule = partial(_naryop_weak_type_rule, name)
  prim = standard_primitive(shape_rule, dtype_rule, name,
                            weak_type_rule=weak_type_rule)
  batching.defbroadcasting(prim)
  masking.defnaryop(prim)
  pe.padding_rules[prim] = lambda _, __, *xs, **kw: [prim.bind(*xs, **kw)]
  return prim
