def unmapped_aval(size: AxisSize, axis_name, axis: int | None,
                  aval: AbstractValue) -> AbstractValue:
  _, handler = aval_mapping_handlers.get(type(aval), (None, None))
  if handler is not None:
    return handler(size, axis_name, axis, aval)
  else:
    raise TypeError(f"no unmapping handler for {aval} of type {type(aval)}")
