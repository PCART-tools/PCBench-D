def _jaxpr_type_to_callable_annotation(jaxpr: Jaxpr) -> InputType:
  idxs = {v: DBIdx(i) for i, v in enumerate((*jaxpr.constvars, *jaxpr.invars))}
  out = [(v.aval.update(shape=tuple(idxs.get(d, d) for d in v.aval.shape))  # type: ignore
          if type(v.aval) is DShapedArray else v.aval, True)
         for v in jaxpr.invars]
  return tuple(out)
