@util.implements(np.histogram)
def histogram(a: ArrayLike, bins: ArrayLike = 10,
              range: Sequence[ArrayLike] | None = None,
              weights: ArrayLike | None = None,
              density: bool | None = None) -> tuple[Array, Array]:
  if weights is None:
    util.check_arraylike("histogram", a, bins)
    a, = util.promote_dtypes_inexact(a)
    weights = ones_like(a)
  else:
    util.check_arraylike("histogram", a, bins, weights)
    if shape(a) != shape(weights):
      raise ValueError("weights should have the same shape as a.")
    a, weights = util.promote_dtypes_inexact(a, weights)

  bin_edges = histogram_bin_edges(a, bins, range, weights)
  bin_idx = searchsorted(bin_edges, a, side='right')
  bin_idx = where(a == bin_edges[-1], len(bin_edges) - 1, bin_idx)
  counts = zeros(len(bin_edges), weights.dtype).at[bin_idx].add(weights)[1:]
  if density:
    bin_widths = diff(bin_edges)
    counts = counts / bin_widths / counts.sum()
  return counts, bin_edges
