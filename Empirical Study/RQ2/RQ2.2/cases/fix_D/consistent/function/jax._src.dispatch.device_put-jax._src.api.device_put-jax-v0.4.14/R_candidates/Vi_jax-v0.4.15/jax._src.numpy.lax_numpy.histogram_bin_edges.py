@util._wraps(np.histogram_bin_edges)
def histogram_bin_edges(a: ArrayLike, bins: ArrayLike = 10,
                        range: None | Array | Sequence[ArrayLike] = None,
                        weights: ArrayLike | None = None) -> Array:
  del weights  # unused, because string bins is not supported.
  if isinstance(bins, str):
    raise NotImplementedError("string values for `bins` not implemented.")
  util.check_arraylike("histogram_bin_edges", a, bins)
  arr = ravel(a)
  dtype = dtypes.to_inexact_dtype(arr.dtype)
  if _ndim(bins) == 1:
    return asarray(bins, dtype=dtype)

  bins_int = core.concrete_or_error(operator.index, bins,
                                    "bins argument of histogram_bin_edges")
  if range is None:
    range = [arr.min(), arr.max()]
  range = asarray(range, dtype=dtype)
  if shape(range) != (2,):
    raise ValueError(f"`range` must be either None or a sequence of scalars, got {range}")
  range = (where(reductions.ptp(range) == 0, range[0] - 0.5, range[0]),
           where(reductions.ptp(range) == 0, range[1] + 0.5, range[1]))
  assert range is not None
  return linspace(range[0], range[1], bins_int + 1, dtype=dtype)
