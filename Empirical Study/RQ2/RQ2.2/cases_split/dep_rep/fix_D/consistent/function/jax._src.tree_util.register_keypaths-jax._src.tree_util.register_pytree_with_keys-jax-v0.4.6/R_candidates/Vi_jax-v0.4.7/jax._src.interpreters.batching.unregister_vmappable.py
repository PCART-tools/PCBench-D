def unregister_vmappable(data_type: Type) -> None:
  spec_type, axis_size_type = vmappables.pop(data_type)
  spec_types.remove(spec_type)
  del to_elt_handlers[data_type]
  del from_elt_handlers[data_type]
  if axis_size_type in make_iota_handlers:
    del make_iota_handlers[axis_size_type]
