def _memcpy(axis, num, src, dst, offset):
  def body(i, dst):
    update = slicing.dynamic_index_in_dim(src, i, axis)
    return slicing.dynamic_update_index_in_dim(dst, update, i + offset, axis)
  return fori_loop(0, num, body, dst)
