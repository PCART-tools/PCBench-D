@_wraps(np.histogramdd)
def histogramdd(sample, bins=10, range=None, weights=None, density=None):
  if weights is None:
    _check_arraylike("histogramdd", sample)
    sample, = _promote_dtypes_inexact(sample)
  else:
    _check_arraylike("histogramdd", sample, weights)
    if weights.shape != sample.shape[:1]:
      raise ValueError("should have one weight for each sample.")
    sample, weights = _promote_dtypes_inexact(sample, weights)
  N, D = shape(sample)

  if range is not None and (
      len(range) != D or _any(r is not None and len(r) != 2 for r in range)):
    raise ValueError(f"For sample.shape={(N, D)}, range must be a sequence "
                     f"of {D} pairs or Nones; got range={range}")

  try:
    num_bins = len(bins)
    if num_bins != D:
      raise ValueError("should be a bin for each dimension.")
  except TypeError:
    # when bin_size is integer, the same bin is used for each dimension
    bins = D * [bins]

  bin_idx_by_dim = D * [None]
  nbins = np.empty(D, int)
  bin_edges_by_dim = D * [None]
  dedges = D * [None]

  for i in builtins.range(D):
    range_i = None if range is None else range[i]
    bin_edges = histogram_bin_edges(sample[:, i], bins[i], range_i, weights)
    bin_idx = searchsorted(bin_edges, sample[:, i], side='right')
    bin_idx = where(sample[:, i] == bin_edges[-1], bin_idx - 1, bin_idx)
    bin_idx_by_dim[i] = bin_idx
    nbins[i] = len(bin_edges) + 1
    bin_edges_by_dim[i] = bin_edges
    dedges[i] = diff(bin_edges_by_dim[i])

  xy = ravel_multi_index(bin_idx_by_dim, nbins, mode='clip')
  hist = bincount(xy, weights, length=nbins.prod())
  hist = reshape(hist, nbins)
  core = D*(slice(1, -1),)
  hist = hist[core]

  if density:
    hist = hist.astype(sample.dtype)
    hist /= hist.sum()
    for norm in ix_(*dedges):
      hist /= norm

  return hist, bin_edges_by_dim
