def _getslice_padding_rule(in_avals, out_avals, x, lo, hi):
  xx = lax.concatenate([x, x], 0)
  return [dynamic_slice_in_dim(xx, lo, x.shape[0])]
