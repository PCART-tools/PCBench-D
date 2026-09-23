def _pmap_axis_subst(params, subst, traverse):
  if 'call_jaxpr' not in params:
    return params
  if not traverse:
    return params
  def shadowed_subst(name):
    return (name,) if name in params['axis_name'] else subst(name)
  with maybe_extend_axis_env(params['axis_name'],
                             params['global_axis_size'], None):
    new_jaxpr = core.subst_axis_names_jaxpr(params['call_jaxpr'],
                                            shadowed_subst)
  return dict(params, call_jaxpr=new_jaxpr)
