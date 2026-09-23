def _complete_specs(
    args: Sequence[Any], partial_specs: list[dict[int, AbstractedAxisName]]
  ) -> list[dict[int, AbstractedAxisName]]:
  # The abstracted axes specification in `partial_specs` is partial in the sense
  # that there could be additional axis abstraction represented in `args` due to
  # Tracers existing in the shapes of elements of `args`. The purpose of this
  # function is to produce a full specification, for each argument mapping any
  # abstracted axis positions to a name, introducing new names as needed for
  # Tracers in axis sizes which don't already correspond to abstracted axis
  # names (with one new name per unique Tracer object id).

  # Identify each user-supplied name in partial_specs with a size.
  sizes: dict[AbstractedAxisName, int | DynamicJaxprTracer] = {}
  for x, spec in zip(args, partial_specs):
    for i, name in spec.items():
      d = sizes.setdefault(name, x.shape[i])
      if d is not x.shape[i] and d != x.shape[i]: raise TypeError

  # Introduce new names as needed for Tracers in shapes.
  named_tracers: dict[TracerId, AbstractedAxisName] = {
      id(d): name for name, d in sizes.items() if isinstance(d, Tracer)}
  specs: list[dict[int, AbstractedAxisName]] = []
  for x, spec in zip(args, partial_specs):
    if isinstance(get_aval(x), DShapedArray):
      spec = dict(spec)
      for i, d in enumerate(x.shape):
        if isinstance(d, Tracer):
          spec[i] = named_tracers.get(id(d), TracerAsName(d))
    specs.append(spec)

  # Assert that `specs` is now complete in the sense that there are no Tracers
  # which don't correspond to an AbstractedAxisName.
  assert all(not spec or not any(isinstance(d, Tracer) and i not in spec
                                 for i, d in enumerate(x.shape))
             for x, spec in zip(args, specs))
  return specs
