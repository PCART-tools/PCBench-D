@_wraps(
    osp_interpolate.RegularGridInterpolator,
    lax_description="""
In the JAX version, `bounds_error` defaults to and must always be `False` since no
bound error may be raised under JIT.

Furthermore, in contrast to SciPy no input validation is performed.
""")
class RegularGridInterpolator:
  # Based on SciPy's implementation which in turn is originally based on an
  # implementation by Johannes Buchner

  def __init__(self,
               points,
               values,
               method="linear",
               bounds_error=False,
               fill_value=nan):
    if method not in ("linear", "nearest"):
      raise ValueError(f"method {method!r} is not defined")
    self.method = method
    self.bounds_error = bounds_error
    if self.bounds_error:
      raise NotImplementedError("`bounds_error` takes no effect under JIT")

    _check_arraylike("RegularGridInterpolator", values)
    if len(points) > values.ndim:
      ve = f"there are {len(points)} point arrays, but values has {values.ndim} dimensions"
      raise ValueError(ve)

    values, = _promote_dtypes_inexact(values)

    if fill_value is not None:
      _check_arraylike("RegularGridInterpolator", fill_value)
      fill_value = asarray(fill_value)
      if not can_cast(fill_value.dtype, values.dtype, casting='same_kind'):
        ve = "fill_value must be either 'None' or of a type compatible with values"
        raise ValueError(ve)
    self.fill_value = fill_value

    # TODO: assert sanity of `points` similar to SciPy but in a JIT-able way
    _check_arraylike("RegularGridInterpolator", *points)
    self.grid = tuple(asarray(p) for p in points)
    self.values = values

  @_wraps(osp_interpolate.RegularGridInterpolator.__call__, update_doc=False)
  def __call__(self, xi, method=None):
    method = self.method if method is None else method
    if method not in ("linear", "nearest"):
      raise ValueError(f"method {method!r} is not defined")

    ndim = len(self.grid)
    xi = _ndim_coords_from_arrays(xi, ndim=ndim)
    if xi.shape[-1] != len(self.grid):
      raise ValueError("the requested sample points xi have dimension"
                       f" {xi.shape[1]}, but this RegularGridInterpolator has"
                       f" dimension {ndim}")

    xi_shape = xi.shape
    xi = xi.reshape(-1, xi_shape[-1])

    indices, norm_distances, out_of_bounds = self._find_indices(xi.T)
    if method == "linear":
      result = self._evaluate_linear(indices, norm_distances)
    elif method == "nearest":
      result = self._evaluate_nearest(indices, norm_distances)
    else:
      raise AssertionError("method must be bound")
    if not self.bounds_error and self.fill_value is not None:
      bc_shp = result.shape[:1] + (1,) * (result.ndim - 1)
      result = where(out_of_bounds.reshape(bc_shp), self.fill_value, result)

    return result.reshape(xi_shape[:-1] + self.values.shape[ndim:])

  def _evaluate_linear(self, indices, norm_distances):
    # slice for broadcasting over trailing dimensions in self.values
    vslice = (slice(None),) + (None,) * (self.values.ndim - len(indices))

    # find relevant values
    # each i and i+1 represents a edge
    edges = product(*[[i, i + 1] for i in indices])
    values = asarray(0.)
    for edge_indices in edges:
      weight = asarray(1.)
      for ei, i, yi in zip(edge_indices, indices, norm_distances):
        weight *= where(ei == i, 1 - yi, yi)
      values += self.values[edge_indices] * weight[vslice]
    return values

  def _evaluate_nearest(self, indices, norm_distances):
    idx_res = [
        where(yi <= .5, i, i + 1) for i, yi in zip(indices, norm_distances)
    ]
    return self.values[tuple(idx_res)]

  def _find_indices(self, xi):
    # find relevant edges between which xi are situated
    indices = []
    # compute distance to lower edge in unity units
    norm_distances = []
    # check for out of bounds xi
    out_of_bounds = zeros((xi.shape[1],), dtype=bool)
    # iterate through dimensions
    for x, g in zip(xi, self.grid):
      i = searchsorted(g, x) - 1
      i = where(i < 0, 0, i)
      i = where(i > g.size - 2, g.size - 2, i)
      indices.append(i)
      norm_distances.append((x - g[i]) / (g[i + 1] - g[i]))
      if not self.bounds_error:
        out_of_bounds += x < g[0]
        out_of_bounds += x > g[-1]
    return indices, norm_distances, out_of_bounds
