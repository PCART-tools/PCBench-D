def naryop(result_dtype, accepted_dtypes, name):
  dtype_rule = partial(naryop_dtype_rule, result_dtype, accepted_dtypes, name)
  shape_rule = partial(broadcasting_shape_rule, name)
  weak_type_rule = partial(_naryop_weak_type_rule, name)
  prim = standard_primitive(shape_rule, dtype_rule, name,
                            weak_type_rule=weak_type_rule)
  batching.defbroadcasting(prim)
  pe.def_trivial_padding(prim)
  return prim
