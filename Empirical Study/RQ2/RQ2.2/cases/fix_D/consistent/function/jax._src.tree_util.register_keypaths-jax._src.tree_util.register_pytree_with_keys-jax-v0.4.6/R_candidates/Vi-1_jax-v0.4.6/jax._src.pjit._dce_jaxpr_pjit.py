@weakref_lru_cache
def _dce_jaxpr_pjit(
    jaxpr: core.ClosedJaxpr, used_outputs: Tuple[bool]
) -> Tuple[core.ClosedJaxpr, List[bool]]:
  new_jaxpr, used_inputs = pe.dce_jaxpr(jaxpr.jaxpr, used_outputs)
  return core.ClosedJaxpr(new_jaxpr, jaxpr.consts), used_inputs
