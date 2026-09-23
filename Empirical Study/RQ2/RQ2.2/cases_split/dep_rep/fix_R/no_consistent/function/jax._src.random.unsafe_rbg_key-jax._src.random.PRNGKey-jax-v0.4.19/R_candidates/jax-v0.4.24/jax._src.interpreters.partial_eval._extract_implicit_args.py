def _extract_implicit_args(
    trace: DynamicJaxprTrace, in_type: Sequence[tuple[AbstractValue, bool]],
    explicit_tracers: Sequence[DynamicJaxprTracer]
  ) -> Sequence[DynamicJaxprTracer]:
  # First, construct a list to represent the full argument list, leaving the
  # implicit arguments as Nones for now.
  explicit_tracers_ = iter(explicit_tracers)
  tracers = [next(explicit_tracers_) if expl else None for _, expl in in_type]
  assert next(explicit_tracers_, None) is None
  del explicit_tracers_

  # Next, populate the implicit arguments using DBIdxs in in_type.
  for i, (aval, explicit) in enumerate(in_type):
    if not explicit or not isinstance(aval, DShapedArray):
      continue  # can't populate an implicit argument
    tracer = tracers[i]
    assert tracer is not None
    for d1, d2 in zip(aval.shape, tracer.aval.shape):
      if isinstance(d1, DBIdx):
        if tracers[d1.val] is None:
          tracers[d1.val] = trace.instantiate_const(d2)
        assert tracers[d1.val] is trace.instantiate_const(d2)
  assert all(t is not None for t in tracers)
  return [t for t, (_, e) in zip(tracers, in_type) if not e]  # type: ignore
