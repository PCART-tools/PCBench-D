def mapped_aval(size: AxisSize, axis: int | None,
                aval: AbstractValue) -> AbstractValue:
  handler, _ = aval_mapping_handlers.get(type(aval), (None, None))
  if handler is not None:
    return handler(size, axis, aval)
  else:
    raise TypeError(f"no mapping handler for {aval} of type {type(aval)}")
