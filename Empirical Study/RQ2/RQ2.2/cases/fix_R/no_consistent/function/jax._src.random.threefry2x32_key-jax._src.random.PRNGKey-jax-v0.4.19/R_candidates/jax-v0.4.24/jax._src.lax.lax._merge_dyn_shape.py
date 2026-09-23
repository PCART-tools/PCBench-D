def _merge_dyn_shape(
    static_shape: Sequence[int | None],
    dyn_shape: Sequence[Any],
  ) -> tuple[int | mlir.Value | core.Tracer, ...]:
  # Replace Nones in static_shape with elements of dyn_shape, in order
  dyn_shape_it = iter(dyn_shape)
  shape = tuple(next(dyn_shape_it) if d is None else d for d in static_shape)
  assert next(dyn_shape_it, None) is None
  return shape
