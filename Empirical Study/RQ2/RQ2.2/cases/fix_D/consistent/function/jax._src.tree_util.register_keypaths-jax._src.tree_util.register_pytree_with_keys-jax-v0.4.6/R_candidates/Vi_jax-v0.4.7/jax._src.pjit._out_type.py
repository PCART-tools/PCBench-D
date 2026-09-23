def _out_type(jaxpr: core.ClosedJaxpr) -> List[core.AbstractValue]:
  out = []
  in_idx = {v: i for i, v in enumerate(jaxpr.jaxpr.invars)}
  out_idx = {x: i for i, x in enumerate(jaxpr.jaxpr.invars)
             if type(x) is core.Var}
  for x in jaxpr.jaxpr.outvars:
    aval = x.aval
    if type(aval) is core.DShapedArray:
      shape = [core.InDBIdx(in_idx[d]) if d in in_idx else
               core.OutDBIdx(out_idx[d]) if d in out_idx else
               d for d in x.aval.shape]
      aval = aval.update(shape=tuple(shape))
    out.append(aval)
  return out
