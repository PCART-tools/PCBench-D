@random_split_p.def_abstract_eval
def random_split_abstract_eval(keys_aval, *, shape):
  return keys_shaped_array(keys_aval.dtype._impl, (*keys_aval.shape, *shape))
