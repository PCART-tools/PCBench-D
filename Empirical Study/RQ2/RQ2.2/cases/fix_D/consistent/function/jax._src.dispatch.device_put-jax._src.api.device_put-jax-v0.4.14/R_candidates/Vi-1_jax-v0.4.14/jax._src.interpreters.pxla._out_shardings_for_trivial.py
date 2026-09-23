def _out_shardings_for_trivial(
    jaxpr: core.Jaxpr, consts: Sequence[Any],
    in_shardings: Sequence[sharding_impls.XLACompatibleSharding],
    device_assignment: Sequence[xc.Device],
  ) -> list[sharding_impls.XLACompatibleSharding]:
  # For each jaxpr output, compute a Sharding by:
  #   * if the output is a forwarded input, get the corresponding in_sharding;
  #   * if the output is a constant Array, get its .sharding attribute;
  #   * otherwise, the output is a literal or numpy.ndarray constant, so give it
  #     a replicated sharding
  from jax._src import array

  if len(device_assignment) > 1:
    rep = sharding_impls.GSPMDSharding.get_replicated(device_assignment)
    in_shardings = tuple(
        i._original_sharding if hasattr(i, '_original_sharding') else i
        for i in in_shardings)
  else:
    dev, = device_assignment
    rep = sharding_impls.SingleDeviceSharding(dev)
    in_shardings = (sharding_impls.SingleDeviceSharding(dev),) * len(in_shardings)

  shardings: dict[core.Var, sharding_impls.XLACompatibleSharding] = {}
  for constvar, constval in zip(jaxpr.constvars, consts):
    if isinstance(constval, array.ArrayImpl):
      shardings[constvar] = constval.sharding
  map(shardings.setdefault, jaxpr.invars, in_shardings)
  return [rep if isinstance(x, core.Literal) else shardings.get(x, rep)
          for x in jaxpr.outvars]
