def _out_shardings_for_trivial(
    jaxpr: core.Jaxpr, consts: Sequence[Any],
    in_shardings: Sequence[sharding_internal.XLACompatibleSharding],
    device_assignment: Sequence[xc.Device],
  ) -> List[sharding_internal.XLACompatibleSharding]:
  # For each jaxpr output, compute a Sharding by:
  #   * if the output is a forwarded input, get the corresponding in_sharding;
  #   * if the output is a constant Array, get its .sharding attribute;
  #   * otherwise, the output is a literal or numpy.ndarray constant, so give it
  #     a replicated sharding
  from jax._src import array

  rep = sharding_internal.GSPMDSharding(
      device_assignment, sharding_internal._get_replicated_op_sharding())
  shardings: Dict[core.Var, sharding_internal.XLACompatibleSharding] = {}
  for constvar, constval in zip(jaxpr.constvars, consts):
    if isinstance(constval, array.ArrayImpl):
      shardings[constvar] = constval.sharding
  map(shardings.setdefault, jaxpr.invars, in_shardings)
  return [rep if isinstance(x, core.Literal) else shardings.get(x, rep)
          for x in jaxpr.outvars]
