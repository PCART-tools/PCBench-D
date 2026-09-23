def _collect_implicit(
    args: Sequence[Any], specs: list[dict[int, AbstractedAxisName]]
  ) -> tuple[dict[AbstractedAxisName, DBIdx], list[AbstractValue]]:
  # Given an explicit argument list and a specification of abstracted axes, we
  # want to produce an InputType by identifying AbstractedAxisNames with DBIdxs
  # and figuring out which AbstractedAxisNames correspond to implicit arguments.

  idxs: dict[AbstractedAxisName, DBIdx] = {}
  implicit_types: list[AbstractValue] = []
  explicit_tracers: dict[TracerId, int] = {}
  counter = it.count()

  # Add implicit arguments to idxs.
  for explicit_idx, (x, spec) in enumerate(zip(args, specs)):
    for i, name in spec.items():
      if name not in idxs and id(x.shape[i]) not in explicit_tracers:
        idxs[name] = DBIdx(next(counter))
        implicit_types.append(raise_to_shaped(get_aval(x.shape[i])))
    if isinstance(x, Tracer):
      explicit_tracers.setdefault(id(x), explicit_idx)  # use the first

  # Now that we know the implicit args, add explicit args to idxs.
  offset = len(implicit_types)
  for x, spec in zip(args, specs):
    for i, name in spec.items():
      if id(x.shape[i]) in explicit_tracers:
        idxs.setdefault(name, DBIdx(offset + explicit_tracers[id(x.shape[i])]))

  return idxs, implicit_types
