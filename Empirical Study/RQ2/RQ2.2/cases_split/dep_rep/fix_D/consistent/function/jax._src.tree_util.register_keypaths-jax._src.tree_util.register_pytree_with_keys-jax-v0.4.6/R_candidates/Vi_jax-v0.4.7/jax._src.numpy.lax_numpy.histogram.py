@util._wraps(np.histogram)
def histogram(a: ArrayLike, bins: ArrayLike = 10,
              range: Optional[Sequence[ArrayLike]] = None,
              weights: Optional[ArrayLike] = None,
              density: Optional[bool] = None) -> Tuple[Array, Array]:
  if weights is None:
    util.check_arraylike("histogram", a, bins)
    a = ravel(*util.promote_dtypes_inexact(a))
    weights = ones_like(a)
  else:
    util.check_arraylike("histogram", a, bins, weights)
    if shape(a) != shape(weights):
      raise ValueError("weights should have the same shape as a.")
    a, weights = map(ravel, util.promote_dtypes_inexact(a, weights))

  bin_edges = histogram_bin_edges(a, bins, range, weights)
  bin_idx = searchsorted(bin_edges, a, side='right')
  bin_idx = where(a == bin_edges[-1], len(bin_edges) - 1, bin_idx)
  counts = bincount(bin_idx, weights, length=len(bin_edges))[1:]
  if density:
    bin_widths = diff(bin_edges)
    counts = counts / bin_widths / counts.sum()
  return counts, bin_edges
