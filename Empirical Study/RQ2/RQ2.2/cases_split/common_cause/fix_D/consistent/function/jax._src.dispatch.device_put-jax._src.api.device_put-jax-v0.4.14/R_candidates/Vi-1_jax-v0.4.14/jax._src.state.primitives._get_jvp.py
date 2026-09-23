def _get_jvp(primals: list[Any], tangents: list[Any], **params: Any):
  ref_primal, *idx = primals
  assert isinstance(ref_primal.aval, AbstractRef)
  ref_tangent, *_ = tangents
  assert isinstance(ref_tangent.aval, AbstractRef)
  return (get_p.bind(ref_primal, *idx, **params),
          get_p.bind(ref_tangent, *idx, **params))  # type: ignore[arg-type]
