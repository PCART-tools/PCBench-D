def _convert_element_type_jvp_rule(tangent, operand , *, new_dtype, weak_type):
  if core.primal_dtype_to_tangent_dtype(new_dtype) == dtypes.float0:
    return ad_util.Zero(tangent.aval.update(dtype=dtypes.float0, weak_type=False))
  else:
    return convert_element_type_p.bind(tangent, new_dtype=new_dtype,
                                       weak_type=weak_type)
