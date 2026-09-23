def _swap_jvp(primals: list[Any], tangents: list[Any], **params: Any):
  ref_primal, x_primal, *idx = primals
  assert isinstance(ref_primal.aval, AbstractRef)
  ref_tangent, x_tangent, *_ = tangents
  assert isinstance(ref_tangent.aval, AbstractRef)
  x_tangent = ad_util.instantiate(x_tangent)
  return (swap_p.bind(ref_primal, x_primal, *idx, **params),  # type: ignore[arg-type]
          swap_p.bind(ref_tangent, x_tangent, *idx, **params))  # type: ignore[arg-type]
