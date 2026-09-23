def _pp_idx(context, non_slice_idx, indexed_dims):
  idx_iter = iter(non_slice_idx)
  idx = ','.join(core.pp_var(next(idx_iter), context) if indexed else ':'
                 for indexed in indexed_dims)
  assert next(idx_iter, None) is None
  return pp.text(idx)
