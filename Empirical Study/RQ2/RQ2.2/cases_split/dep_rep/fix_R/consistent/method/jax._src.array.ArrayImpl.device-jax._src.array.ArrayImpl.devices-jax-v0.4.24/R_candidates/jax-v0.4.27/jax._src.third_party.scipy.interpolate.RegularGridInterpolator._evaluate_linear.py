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
