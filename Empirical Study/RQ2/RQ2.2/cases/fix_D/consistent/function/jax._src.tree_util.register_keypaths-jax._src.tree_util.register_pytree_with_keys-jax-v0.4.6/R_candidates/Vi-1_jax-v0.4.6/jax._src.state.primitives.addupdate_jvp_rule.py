def addupdate_jvp_rule(primals: List[Any], tangents: List[Any], **params: Any):
  ref_primal, x_primal, *idx = primals
  ref_tangent, x_tangent, *_ = tangents
  x_tangent = ad_util.instantiate(x_tangent)
  addupdate_p.bind(ref_primal, x_primal, *idx, **params)
  addupdate_p.bind(ref_tangent, x_tangent, *idx, **params)
  return [], []
