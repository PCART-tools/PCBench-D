@random_fold_in_p.def_abstract_eval
def random_fold_in_abstract_eval(keys_aval, msgs_aval):
  shape = lax_internal.broadcasting_shape_rule(
      'random_fold_in', keys_aval, msgs_aval)
  named_shape = lax_utils.standard_named_shape_rule(keys_aval, msgs_aval)
  return core.ShapedArray(shape, keys_aval.dtype, named_shape=named_shape)
