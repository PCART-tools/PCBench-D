@random_split_p.def_abstract_eval
def random_split_abstract_eval(keys_aval, *, count):
  return keys_shaped_array(keys_aval.dtype.impl, (*keys_aval.shape, count))
