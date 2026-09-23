def _merge_dyn_shape(
    static_shape: Sequence[Optional[int]],
    dyn_shape: Sequence[Any],
  ) -> Tuple[Union[int, mlir.Value], ...]:
  # Replace Nones in static_shape with elements of dyn_shape, in order
  dyn_shape_it = iter(dyn_shape)
  shape = tuple(next(dyn_shape_it) if d is None else d for d in static_shape)
  assert next(dyn_shape_it, None) is None
  return shape
