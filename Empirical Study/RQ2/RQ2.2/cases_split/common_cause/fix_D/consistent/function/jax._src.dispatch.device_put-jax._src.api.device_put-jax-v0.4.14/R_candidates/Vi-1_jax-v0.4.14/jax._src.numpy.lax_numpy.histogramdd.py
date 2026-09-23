@util._wraps(np.histogramdd)
def histogramdd(sample: ArrayLike, bins: Union[ArrayLike, list[ArrayLike]] = 10,
                range: Optional[Sequence[Union[None, Array, Sequence[ArrayLike]]]] = None,
                weights: Optional[ArrayLike] = None,
                density: Optional[bool] = None) -> tuple[Array, list[Array]]:
  if weights is None:
    util.check_arraylike("histogramdd", sample)
    sample, = util.promote_dtypes_inexact(sample)
  else:
    util.check_arraylike("histogramdd", sample, weights)
    if shape(weights) != shape(sample)[:1]:
      raise ValueError("should have one weight for each sample.")
    sample, weights = util.promote_dtypes_inexact(sample, weights)
  N, D = shape(sample)

  if range is not None and (
      len(range) != D or any(r is not None and shape(r)[0] != 2 for r in range)):  # type: ignore[arg-type]
    raise ValueError(f"For sample.shape={(N, D)}, range must be a sequence "
                     f"of {D} pairs or Nones; got {range=}")

  try:
    num_bins = len(bins)  # type: ignore[arg-type]
  except TypeError:
    # when bin_size is integer, the same bin is used for each dimension
    bins_per_dimension: list[ArrayLike] = D * [bins]  # type: ignore[assignment]
  else:
    if num_bins != D:
      raise ValueError("should be a bin for each dimension.")
    bins_per_dimension = list(bins)  # type: ignore[arg-type]

  bin_idx_by_dim: list[Array] = []
  bin_edges_by_dim: list[Array] = []

  for i in builtins.range(D):
    range_i = None if range is None else range[i]
    bin_edges = histogram_bin_edges(sample[:, i], bins_per_dimension[i], range_i, weights)
    bin_idx = searchsorted(bin_edges, sample[:, i], side='right')
    bin_idx = where(sample[:, i] == bin_edges[-1], bin_idx - 1, bin_idx)
    bin_idx_by_dim.append(bin_idx)
    bin_edges_by_dim.append(bin_edges)

  nbins = tuple(len(bin_edges) + 1 for bin_edges in bin_edges_by_dim)
  dedges = [diff(bin_edges) for bin_edges in bin_edges_by_dim]

  xy = ravel_multi_index(tuple(bin_idx_by_dim), nbins, mode='clip')
  hist = bincount(xy, weights, length=math.prod(nbins))
  hist = reshape(hist, nbins)
  core = D*(slice(1, -1),)
  hist = hist[core]

  if density:
    hist = hist.astype(sample.dtype)
    hist /= hist.sum()
    for norm in ix_(*dedges):
      hist /= norm

  return hist, bin_edges_by_dim
