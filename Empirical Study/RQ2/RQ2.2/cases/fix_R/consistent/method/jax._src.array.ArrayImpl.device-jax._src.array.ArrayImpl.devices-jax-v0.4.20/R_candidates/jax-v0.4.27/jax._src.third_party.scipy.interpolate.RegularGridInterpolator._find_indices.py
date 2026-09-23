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
