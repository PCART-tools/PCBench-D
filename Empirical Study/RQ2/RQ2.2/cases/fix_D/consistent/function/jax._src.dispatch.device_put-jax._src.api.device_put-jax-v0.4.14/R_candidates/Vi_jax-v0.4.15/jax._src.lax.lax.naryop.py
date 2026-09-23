def naryop(result_dtype, accepted_dtypes, name, allow_extended_dtype=False,
           require_same_dtypes=False):
  dtype_rule = partial(naryop_dtype_rule, result_dtype, accepted_dtypes, name,
                       allow_extended_dtype=allow_extended_dtype,
                       require_same=require_same_dtypes)
  shape_rule = partial(broadcasting_shape_rule, name)
  weak_type_rule = partial(_naryop_weak_type_rule, name)
  prim = standard_primitive(shape_rule, dtype_rule, name,
                            weak_type_rule=weak_type_rule)
  batching.defbroadcasting(prim)
  pe.def_trivial_padding(prim)
  return prim
