def _pmap_unmapped_aval(size: core.AxisSize, axis_name, axis: int | None,
                       aval: core.AbstractValue) -> core.AbstractValue:
  if not config.pmap_no_rank_reduction.value:
    return core.unmapped_aval(size, axis_name, axis, aval)

  _, handler = _pmap_aval_mapping_handlers.get(type(aval), (None, None))
  if handler is not None:
    return handler(size, axis_name, axis, aval)
  else:
    raise TypeError(f"no unmapping handler for {aval} of type {type(aval)}")
