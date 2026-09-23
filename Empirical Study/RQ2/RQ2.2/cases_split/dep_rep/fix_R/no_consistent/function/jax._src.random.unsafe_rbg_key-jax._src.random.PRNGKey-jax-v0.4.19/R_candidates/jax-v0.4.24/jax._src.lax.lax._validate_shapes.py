def _validate_shapes(shapes: Sequence[Shape]):
  def _check_static_shape(shape: Shape):
    checked = canonicalize_shape(shape)
    if not all(idx >= 0 for idx in checked):
      msg = f"Only non-negative indices are allowed when broadcasting" \
            f" static shapes, but got shape {shape!r}."
      raise TypeError(msg)

  assert shapes
  if config.dynamic_shapes.value:
    # pass dynamic shapes through unchecked
    return
  else:
    map(_check_static_shape, shapes)
