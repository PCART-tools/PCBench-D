def custom_vmap_abstract_eval(*in_avals, call, **_):
  return call.out_avals
