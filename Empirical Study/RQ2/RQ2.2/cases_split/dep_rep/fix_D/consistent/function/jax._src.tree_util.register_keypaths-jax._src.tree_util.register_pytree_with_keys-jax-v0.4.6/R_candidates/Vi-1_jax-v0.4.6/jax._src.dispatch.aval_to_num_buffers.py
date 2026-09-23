def aval_to_num_buffers(aval: core.AbstractValue) -> int:
  """Returns the number of buffers in the runtime representation of `aval`.

  In general this may differ from the number of buffers in the compiler-IR
  representation of the same value.
  """
  try:
    return num_buffers_handlers[type(aval)](aval)
  except KeyError as err:
    raise TypeError(f"No num_buffers handler for type: {type(aval)}") from err
