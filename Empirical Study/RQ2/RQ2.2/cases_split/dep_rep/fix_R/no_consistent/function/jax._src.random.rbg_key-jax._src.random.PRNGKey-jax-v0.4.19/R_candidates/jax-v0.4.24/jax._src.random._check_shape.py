def _check_shape(name: str, shape: Shape | NamedShape, *param_shapes) -> None:
  shape = core.as_named_shape(shape)

  if param_shapes:
    shape_ = lax.broadcast_shapes(shape.positional, *param_shapes)
    if shape.positional != shape_:
      msg = ("{} parameter shapes must be broadcast-compatible with shape "
             "argument, and the result of broadcasting the shapes must equal "
             "the shape argument, but got result {} for shape argument {}.")
      raise ValueError(msg.format(name, shape_, shape))
