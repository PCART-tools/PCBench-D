def _extract_tracers_dyn_shape(
    shape: Sequence[int | core.Tracer]
  ) -> tuple[list[core.Tracer], list[int | None]]:
  # Given a sequence representing a shape, pull out Tracers, replacing with None
  if config.dynamic_shapes.value:
    # We must gate this behavior under a flag because otherwise the errors
    # raised are different (and have worse source provenance information).
    dyn_shape = [d for d in shape if isinstance(d, core.Tracer)]
    static_shape = [None if isinstance(d, core.Tracer) else d for d in shape]
    return dyn_shape, static_shape
  else:
    return [], list(shape)  # type: ignore
