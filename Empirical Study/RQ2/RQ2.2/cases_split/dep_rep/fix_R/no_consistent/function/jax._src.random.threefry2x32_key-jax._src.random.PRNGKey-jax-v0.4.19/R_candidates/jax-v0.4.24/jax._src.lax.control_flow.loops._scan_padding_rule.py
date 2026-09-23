def _scan_padding_rule(in_avals, out_avals, *args, jaxpr, **params):
  return scan_p.bind(*args, jaxpr=_cached_scan_pad_jaxpr(jaxpr), **params)
