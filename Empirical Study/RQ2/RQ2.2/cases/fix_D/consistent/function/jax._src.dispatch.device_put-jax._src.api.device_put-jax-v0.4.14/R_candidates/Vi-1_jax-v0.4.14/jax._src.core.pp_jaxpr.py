def pp_jaxpr(jaxpr, context: JaxprPpContext, settings: JaxprPpSettings) -> pp.Doc:
  eqns_fn = lambda: pp_eqns(jaxpr.eqns, context, settings)
  return pp_jaxpr_skeleton(jaxpr, eqns_fn, context, settings)
