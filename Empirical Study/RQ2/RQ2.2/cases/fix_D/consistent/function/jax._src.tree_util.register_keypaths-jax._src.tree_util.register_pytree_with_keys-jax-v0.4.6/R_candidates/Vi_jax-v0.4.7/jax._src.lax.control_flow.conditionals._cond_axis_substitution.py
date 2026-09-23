def _cond_axis_substitution(params, subst, traverse):
  if not traverse:
    return params
  branches = tuple(core.subst_axis_names_jaxpr(jaxpr, subst) for jaxpr in params['branches'])
  return dict(params, branches=branches)
