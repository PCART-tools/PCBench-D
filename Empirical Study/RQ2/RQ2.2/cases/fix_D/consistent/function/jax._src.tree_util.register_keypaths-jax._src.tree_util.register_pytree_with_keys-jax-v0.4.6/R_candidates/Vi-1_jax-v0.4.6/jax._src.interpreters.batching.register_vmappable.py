def register_vmappable(data_type: Type, spec_type: Type, axis_size_type: Type,
                       to_elt: Callable, from_elt: Callable,
                       make_iota: Optional[Callable]):
  vmappables[data_type] = (spec_type, axis_size_type)
  spec_types.add(spec_type)
  to_elt_handlers[data_type] = to_elt
  from_elt_handlers[data_type] = from_elt
  if make_iota: make_iota_handlers[axis_size_type] = make_iota
