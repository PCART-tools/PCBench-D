def unop(result_dtype, accepted_dtypes, name):
  dtype_rule = partial(unop_dtype_rule, result_dtype, accepted_dtypes, name)
  weak_type_rule = partial(_naryop_weak_type_rule, name)
  prim = standard_primitive(_attrgetter('shape'), dtype_rule, name,
                            weak_type_rule=weak_type_rule)
  batching.defvectorized(prim)
  pe.def_trivial_padding(prim)
  return prim
