@random_wrap_p.def_abstract_eval
def random_wrap_abstract_eval(base_arr_aval, *, impl):
  shape = base_arr_shape_to_keys_shape(impl, base_arr_aval.shape)
  return keys_shaped_array(impl, shape)
