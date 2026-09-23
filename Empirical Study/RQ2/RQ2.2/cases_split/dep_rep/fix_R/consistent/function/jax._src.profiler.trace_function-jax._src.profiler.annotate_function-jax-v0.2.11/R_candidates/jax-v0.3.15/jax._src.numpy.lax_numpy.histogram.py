@_wraps(np.histogram)
def histogram(a, bins=10, range=None, weights=None, density=None):
  if weights is None:
    _check_arraylike("histogram", a, bins)
    a = ravel(*_promote_dtypes_inexact(a))
    weights = ones_like(a)
  else:
    _check_arraylike("histogram", a, bins, weights)
    if a.shape != weights.shape:
      raise ValueError("weights should have the same shape as a.")
    a, weights = map(ravel, _promote_dtypes_inexact(a, weights))

  bin_edges = histogram_bin_edges(a, bins, range, weights)
  bin_idx = searchsorted(bin_edges, a, side='right')
  bin_idx = where(a == bin_edges[-1], len(bin_edges) - 1, bin_idx)
  counts = bincount(bin_idx, weights, length=len(bin_edges))[1:]
  if density:
    bin_widths = diff(bin_edges)
    counts = counts / bin_widths / counts.sum()
  return counts, bin_edges
