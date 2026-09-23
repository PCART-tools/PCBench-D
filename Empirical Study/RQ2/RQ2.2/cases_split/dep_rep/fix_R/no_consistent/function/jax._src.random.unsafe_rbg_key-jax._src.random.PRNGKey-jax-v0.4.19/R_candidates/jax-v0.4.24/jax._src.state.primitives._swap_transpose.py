def _swap_transpose(g, ref, x, *idx, **params):
  del x  # old value doesn't matter anymore
  # swap transpose is swap
  x_bar = swap_p.bind(ref, ad_util.instantiate(g), *idx, **params)
  return [None, x_bar] + [None] * len(idx)
