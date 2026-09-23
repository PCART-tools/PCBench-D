def broadcast_shapes(*shapes: Tuple[Union[int, core.Tracer], ...]
                     ) -> Tuple[Union[int, core.Tracer], ...]:
  """Returns the shape that results from NumPy broadcasting of `shapes`."""
  # NOTE: We have both cached and uncached versions to handle Tracers in shapes.
  try:
    return _broadcast_shapes_cached(*shapes)
  except:
    return _broadcast_shapes_uncached(*shapes)
