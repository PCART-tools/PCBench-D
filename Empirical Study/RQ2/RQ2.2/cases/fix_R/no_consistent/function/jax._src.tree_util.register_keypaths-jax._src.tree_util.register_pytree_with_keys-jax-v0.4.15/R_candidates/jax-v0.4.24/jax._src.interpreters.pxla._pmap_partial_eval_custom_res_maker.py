def _pmap_partial_eval_custom_res_maker(params_known, aval):
  return core.unmapped_aval(params_known['axis_size'], core.no_axis_name, 0, aval)
