def _all_gather_via_psum(x, *, all_gather_dimension, axis_name, axis_index_groups, axis_size, tiled):
  index = _index_in_group(axis_name, axis_index_groups)
  outs = tree_util.tree_map(partial(_expand, all_gather_dimension, axis_size, index, tiled), x)
  sums = psum(outs, axis_name, axis_index_groups=axis_index_groups)
  # psum casts bool elements to int32; cast back.
  return tree_util.tree_map(lambda o, s: s.astype(o.dtype), outs, sums)
