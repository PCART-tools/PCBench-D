@_wraps(np.histogram_bin_edges)
def histogram_bin_edges(a, bins=10, range=None, weights=None):
  del weights  # unused, because string bins is not supported.
  if isinstance(bins, str):
    raise NotImplementedError("string values for `bins` not implemented.")
  _check_arraylike("histogram_bin_edges", a, bins)
  a = ravel(a)
  dtype = dtypes._to_inexact_dtype(_dtype(a))
  if _ndim(bins) == 1:
    return asarray(bins, dtype=dtype)
  bins = core.concrete_or_error(operator.index, bins,
                                "bins argument of histogram_bin_edges")
  if range is None:
    range = [a.min(), a.max()]
  range = asarray(range, dtype=dtype)
  if range.shape != (2,):
    raise ValueError("`range` must be either None or a sequence of scalars.")
  range = (where(ptp(range) == 0, range[0] - 0.5, range[0]),
           where(ptp(range) == 0, range[1] + 0.5, range[1]))
  return linspace(range[0], range[1], bins + 1, dtype=dtype)
