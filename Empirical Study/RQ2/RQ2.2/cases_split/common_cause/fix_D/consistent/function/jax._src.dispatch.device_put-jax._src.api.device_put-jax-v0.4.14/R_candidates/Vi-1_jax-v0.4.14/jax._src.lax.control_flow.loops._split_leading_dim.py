def _split_leading_dim(i, aval, x):
  assert x.ndim >= 1
  return (slicing.slice_in_dim(x, 0, i),
          slicing.slice_in_dim(x, i, x.shape[0]))
