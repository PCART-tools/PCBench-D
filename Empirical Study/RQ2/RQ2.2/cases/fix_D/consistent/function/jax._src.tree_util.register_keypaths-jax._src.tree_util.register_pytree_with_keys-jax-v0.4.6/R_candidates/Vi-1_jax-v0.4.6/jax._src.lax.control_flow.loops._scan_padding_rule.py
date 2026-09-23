def _scan_padding_rule(in_avals, out_avals, *args, jaxpr, **params):
  padded_jaxpr = core.ClosedJaxpr(*pe.pad_jaxpr(jaxpr.jaxpr, jaxpr.consts))
  return scan_p.bind(*args, jaxpr=padded_jaxpr, **params)
