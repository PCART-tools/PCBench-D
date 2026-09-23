def subst_axis_names(primitive: Primitive, params: ParamDict, subst: AxisSubst, traverse: bool = True) -> ParamDict:
  if primitive in axis_substitution_rules:
    return axis_substitution_rules[primitive](params, subst, traverse)
  if not traverse:
    return params
  # Default implementation: substitute names in all jaxpr parameters
  if isinstance(primitive, MapPrimitive):
    def shadowed_subst(name):
      return (name,) if name == params['axis_name'] else subst(name)
  else:
    shadowed_subst = subst
  jaxpr_params = [(n, v) for n, v in params.items() if isinstance(v, (Jaxpr, ClosedJaxpr))]
  if not jaxpr_params:
    return params
  new_params = dict(params)
  for name, jaxpr in jaxpr_params:
    new_params[name] = subst_axis_names_jaxpr(jaxpr, shadowed_subst)
  return new_params
