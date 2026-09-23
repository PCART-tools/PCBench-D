@util._wraps(np.histogram2d)
def histogram2d(x: ArrayLike, y: ArrayLike, bins: Union[ArrayLike, List[ArrayLike]] = 10,
                range: Optional[Sequence[Union[None, Array, Sequence[ArrayLike]]]]=None,
                weights: Optional[ArrayLike] = None,
                density: Optional[bool] = None) -> Tuple[Array, Array, Array]:
  util._check_arraylike("histogram2d", x, y)
  try:
    N = len(bins)  # type: ignore[arg-type]
  except TypeError:
    N = 1

  if N != 1 and N != 2:
    x_edges = y_edges = asarray(bins)
    bins = [x_edges, y_edges]

  sample = transpose(asarray([x, y]))
  hist, edges = histogramdd(sample, bins, range, weights, density)
  return hist, edges[0], edges[1]
