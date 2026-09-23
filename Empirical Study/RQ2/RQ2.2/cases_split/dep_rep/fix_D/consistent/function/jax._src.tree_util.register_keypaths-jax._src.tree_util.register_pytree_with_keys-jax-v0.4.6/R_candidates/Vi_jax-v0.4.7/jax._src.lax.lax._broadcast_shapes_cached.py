@cache()
def _broadcast_shapes_cached(*shapes: Tuple[int, ...]) -> Tuple[int, ...]:
  return _broadcast_shapes_uncached(*shapes)
