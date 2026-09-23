def jaxpr_has_dp_with_transfer_mem_kind(jaxpr: core.Jaxpr) -> bool:
  for eqn in jaxpr.eqns:
    if (eqn.primitive is dispatch.device_put_p and
        isinstance(eqn.params['device'], sharding_impls.TransferToMemoryKind)):
      return True
  for subjaxpr in core.subjaxprs(jaxpr):
    if jaxpr_has_dp_with_transfer_mem_kind(subjaxpr):
      return True
  return False
