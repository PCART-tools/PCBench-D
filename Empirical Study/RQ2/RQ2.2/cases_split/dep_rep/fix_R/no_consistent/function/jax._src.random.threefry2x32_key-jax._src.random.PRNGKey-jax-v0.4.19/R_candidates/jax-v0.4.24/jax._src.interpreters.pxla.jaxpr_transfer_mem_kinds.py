def jaxpr_transfer_mem_kinds(
    jaxpr: core.Jaxpr) -> Iterator[sharding_impls.TransferToMemoryKind]:
  for eqn in jaxpr.eqns:
    if (eqn.primitive is dispatch.device_put_p and
        isinstance(eqn.params['device'], sharding_impls.TransferToMemoryKind)):
      yield eqn.params['device']
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from jaxpr_transfer_mem_kinds(subjaxpr)
