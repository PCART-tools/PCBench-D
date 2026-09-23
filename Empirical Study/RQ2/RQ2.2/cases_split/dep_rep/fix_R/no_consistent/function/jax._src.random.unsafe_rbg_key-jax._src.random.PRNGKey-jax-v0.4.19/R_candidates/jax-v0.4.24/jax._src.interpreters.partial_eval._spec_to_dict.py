def _spec_to_dict(spec: AbstractedAxesSpec) -> dict[int, AbstractedAxisName]:
  if isinstance(spec, tuple):
    return {i: d for i, d in enumerate(spec) if d is not None}
  else:
    return spec
