def _resource_typing_pjit(avals, params, source_info, resource_env, named_axis_resources):
  jaxpr = params["jaxpr"]
  what = "pjit input"
  if (resource_env is not None and params['resource_env'] is not None and
      resource_env.physical_mesh != params['resource_env'].physical_mesh):
      raise RuntimeError("Changing the physical mesh is not allowed inside pjit.")

  for aval, s in zip(jaxpr.in_avals, params['in_shardings']):
    if is_unspecified(s) or is_auto(s):
      continue
    elif hasattr(s, '_original_sharding') and hasattr(
        s._original_sharding, '_parsed_pspec'):
      parsed_pspec = s._original_sharding._parsed_pspec
    else:
      if resource_env is not None:
        parsed_pspec = parse_flatten_op_sharding(
            s._hlo_sharding, resource_env.physical_mesh)[0]
      else:
        parsed_pspec = None
    if parsed_pspec is not None:
      _check_resources_against_named_axes(what, aval, parsed_pspec,
                                          named_axis_resources)

  pxla.resource_typecheck(
      jaxpr.jaxpr, resource_env, named_axis_resources,
      lambda: (f"a pjit'ed function {params['name']} "
               f"(pjit called at {source_info_util.summarize(source_info)})"))

  what = "pjit output"
  for aval, s in zip(jaxpr.out_avals, params['out_shardings']):
    if is_unspecified(s) or is_auto(s):
      continue
    elif hasattr(s, '_original_sharding') and hasattr(
        s._original_sharding, '_parsed_pspec'):
      parsed_pspec = s._original_sharding._parsed_pspec
    else:
      if resource_env is not None:
        parsed_pspec = parse_flatten_op_sharding(
            s._hlo_sharding, resource_env.physical_mesh)[0]
      else:
        parsed_pspec = None
    if parsed_pspec is not None:
      _check_resources_against_named_axes(what, aval, parsed_pspec,
                                          named_axis_resources)
