@weakref_lru_cache
def _known_jaxpr_fwd(known_jaxpr: core.ClosedJaxpr,
                     fwds_known: Tuple[Optional[int]]) -> core.ClosedJaxpr:
  updated_jaxpr = known_jaxpr.jaxpr.replace(
      outvars=[x for x, i in safe_zip(known_jaxpr.jaxpr.outvars, fwds_known)
               if i is None])
  return known_jaxpr.replace(jaxpr=updated_jaxpr)
