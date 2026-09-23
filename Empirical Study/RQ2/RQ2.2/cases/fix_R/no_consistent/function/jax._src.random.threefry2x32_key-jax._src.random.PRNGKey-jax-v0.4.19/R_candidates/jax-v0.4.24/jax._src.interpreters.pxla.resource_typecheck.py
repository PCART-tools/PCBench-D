def resource_typecheck(jaxpr, resource_env, axis_resources, what_jaxpr_thunk):
  if isinstance(jaxpr, core.ClosedJaxpr):
    jaxpr = jaxpr.jaxpr
  def _check_aval(aval, what_thunk):
    if not hasattr(aval, 'named_shape'):
      return
    resource_to_axis = {}
    for axis in aval.named_shape:
      if axis_resources:
        for resource in axis_resources[axis]:
          if resource in resource_to_axis:
            other_axis = resource_to_axis[resource]
            axis, other_axis = sorted([str(axis), str(other_axis)])
            raise JAXTypeError(
                f"Axes `{axis}` and `{other_axis}` are both mapped to the "
                f"resource `{resource}`, but they coincide in the named_shape "
                f"of {what_thunk()}")
          resource_to_axis[resource] = axis

  what_thunk = lambda: (f"an input to {what_jaxpr_thunk()}")
  for v in jaxpr.constvars:
    _check_aval(v.aval, what_thunk)
  for v in jaxpr.invars:
    _check_aval(v.aval, what_thunk)
  what_thunk = lambda: (f"a value returned from a primitive {eqn.primitive} created "
                        f"at {source_info_util.summarize(eqn.source_info)}")
  rec_what_jaxpr_thunk = lambda: (f"a primitive {eqn.primitive} created at"
                                  f"{source_info_util.summarize(eqn.source_info)}")
  for eqn in jaxpr.eqns:
    typing_rule = custom_resource_typing_rules.get(eqn.primitive, None)
    if typing_rule:
      typing_rule([v.aval for v in eqn.invars], eqn.params, eqn.source_info,
                  resource_env, axis_resources)
    else:
      core.traverse_jaxpr_params(partial(resource_typecheck,
                                         resource_env=resource_env,
                                         axis_resources=axis_resources,
                                         what_jaxpr_thunk=rec_what_jaxpr_thunk),
                                 eqn.params)
    for v in eqn.outvars:
      _check_aval(v.aval, what_thunk)
