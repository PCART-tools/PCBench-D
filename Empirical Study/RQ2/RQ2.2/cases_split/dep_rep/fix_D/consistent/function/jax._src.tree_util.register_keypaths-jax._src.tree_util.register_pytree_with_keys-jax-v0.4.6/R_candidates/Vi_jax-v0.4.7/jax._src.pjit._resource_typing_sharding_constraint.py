def _resource_typing_sharding_constraint(avals, params, source_info,
                                         resource_env, named_axis_resources):
  aval, = avals
  if hasattr(params['sharding'], '_original_sharding'):
    parsed_pspec = params['sharding']._original_sharding._parsed_pspec
  else:
    parsed_pspec = parse_flatten_op_sharding(
        params['sharding']._op_sharding, resource_env.physical_mesh)[0]
  _check_resources_against_named_axes(
    "with_sharding_constraint input", aval, parsed_pspec, named_axis_resources)
