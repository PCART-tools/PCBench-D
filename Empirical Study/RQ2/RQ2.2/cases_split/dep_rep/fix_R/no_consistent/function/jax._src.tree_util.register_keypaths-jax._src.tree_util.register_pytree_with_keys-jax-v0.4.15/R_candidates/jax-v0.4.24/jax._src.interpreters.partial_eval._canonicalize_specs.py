def _canonicalize_specs(
    ndims: Sequence[int], specs: Sequence[AbstractedAxesSpec] | None
  ) -> list[dict[int, AbstractedAxisName]]:
  if specs is None:
    return [{}] * len(ndims)
  else:
    return [_spec_to_dict(s) for n, s in zip(ndims, specs)]
