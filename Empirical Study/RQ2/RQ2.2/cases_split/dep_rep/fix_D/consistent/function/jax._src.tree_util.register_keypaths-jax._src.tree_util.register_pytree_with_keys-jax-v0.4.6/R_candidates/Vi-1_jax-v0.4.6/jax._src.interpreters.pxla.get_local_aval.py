def get_local_aval(global_aval, global_parts: PartitionsOrReplicated,
                   local_parts: PartitionsOrReplicated):
  if global_parts is None:
    return global_aval
  assert local_parts is not None
  local_shape = [_safe_div(dim, _safe_div(ngparts, nlparts))
                 for dim, ngparts, nlparts
                 in safe_zip(global_aval.shape, global_parts, local_parts)]
  return global_aval.update(shape=local_shape)
