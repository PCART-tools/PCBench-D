def global_to_local(positional_semantics, avals, shardings, mesh):
  if config.jax_array:
    return avals
  if isinstance(positional_semantics, pxla._PositionalSemantics):
    positional_semantics = [positional_semantics] * len(shardings)

  out = []
  for aval, s, ps in safe_zip(avals, shardings, positional_semantics):
    if (ps == pxla._PositionalSemantics.GLOBAL or
        pxla.is_op_sharding_replicated(s._op_sharding)):
      out.append(aval)
    else:
      # This path is only taken by host-local values. GDA, Array and fully
      # replicated avals don't go through this code path. To convert global
      # avals to host local avals, round trip it via NamedSharding.
      parsed_pspec = parse_flatten_op_sharding(s._op_sharding, mesh)[0]
      out.append(mesh._global_to_local(get_array_mapping(parsed_pspec), aval))
  return out
