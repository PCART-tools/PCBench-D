def aval_to_xla_shapes(aval: core.AbstractValue) -> Sequence[xc.Shape]:
  try:
    return xla_shape_handlers[type(aval)](aval)
  except KeyError as err:
    raise TypeError(f"No xla_shape_handler for type: {type(aval)}") from err
