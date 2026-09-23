def _xmap_axis_subst(params, subst, traverse):
  if 'call_jaxpr' not in params:  # TODO(apaszke): This feels sketchy, but I'm not sure why
    return params
  if not traverse:
    return params
  def shadowed_subst(name):
    return (name,) if name in params['global_axis_sizes'] else subst(name)
  with core.extend_axis_env_nd(params['global_axis_sizes'].items()):
    new_jaxpr = core.subst_axis_names_jaxpr(params['call_jaxpr'], shadowed_subst)
  return dict(params, call_jaxpr=new_jaxpr)
