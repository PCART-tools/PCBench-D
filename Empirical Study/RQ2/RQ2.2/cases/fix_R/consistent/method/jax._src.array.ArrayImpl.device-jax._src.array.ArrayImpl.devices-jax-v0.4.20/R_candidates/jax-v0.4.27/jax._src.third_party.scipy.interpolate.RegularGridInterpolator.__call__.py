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
