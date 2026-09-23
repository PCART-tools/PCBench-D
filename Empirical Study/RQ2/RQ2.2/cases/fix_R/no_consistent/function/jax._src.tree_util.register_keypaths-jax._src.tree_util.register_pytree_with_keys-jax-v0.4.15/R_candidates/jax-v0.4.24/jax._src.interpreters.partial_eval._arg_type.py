def _arg_type(
    idxs: dict[AbstractedAxisName, DBIdx], x: Any,
    spec: dict[int, AbstractedAxisName]
  ) -> AbstractValue:
  # Produce an AbstractValue by substituting DBIdxs for AbstractedAxisNames.
  aval = get_aval(x)  # aval.shape could contain Tracers
  if not spec: return core.raise_to_shaped(aval)
  shape: list[int | DBIdx] = [idxs[spec[i]] if i in spec else d
                                    for i, d in enumerate(aval.shape)]
  assert not any(isinstance(d, Tracer) for d in shape)
  return DShapedArray(tuple(shape), aval.dtype, False)
