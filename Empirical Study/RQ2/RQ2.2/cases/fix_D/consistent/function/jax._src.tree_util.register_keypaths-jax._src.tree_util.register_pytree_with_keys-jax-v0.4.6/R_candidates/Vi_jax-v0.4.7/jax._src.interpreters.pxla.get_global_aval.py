def get_global_aval(local_aval, global_parts: PartitionsOrReplicated,
                    local_parts: PartitionsOrReplicated):
  if global_parts is None:
    return local_aval
  assert local_parts is not None
  global_shape = [dim * _safe_div(ngparts, nlparts)
                  for dim, ngparts, nlparts
                  in safe_zip(local_aval.shape, global_parts, local_parts)]
  return local_aval.update(shape=global_shape)
