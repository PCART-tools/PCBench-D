def _update_annotation(
    f: lu.WrappedFun,
    orig_type: tuple[tuple[core.AbstractValue, bool], ...] | None,
    explicit_nonzeros: list[bool]
  ) -> lu.WrappedFun:
  if orig_type is None:
    return f
  # By convention, `explicit_nonzeros` only accounts for explicit arguments.
  assert len(explicit_nonzeros) == sum(explicit for _, explicit in orig_type)
  # Implicit arguments never have tangents, so generate the tangent part of the
  # type annotation from explicit arguments only.
  explicit_avals = [aval for aval, explicit in orig_type if explicit]
  tan_types = [(aval.at_least_vspace(), True)
               for nz, aval in zip(explicit_nonzeros, explicit_avals) if nz]
  return lu.annotate(f, (*orig_type, *tan_types))
