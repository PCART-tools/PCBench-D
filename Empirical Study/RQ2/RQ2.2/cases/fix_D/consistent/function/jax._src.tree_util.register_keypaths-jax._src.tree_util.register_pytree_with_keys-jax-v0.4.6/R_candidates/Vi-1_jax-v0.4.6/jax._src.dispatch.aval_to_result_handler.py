def aval_to_result_handler(sticky_device: Optional[Device],
                           aval: core.AbstractValue) -> ResultHandler:
  try:
    return result_handlers[type(aval)](sticky_device, aval)
  except KeyError as err:
    raise TypeError(f"No result handler for type: {type(aval)}") from err
