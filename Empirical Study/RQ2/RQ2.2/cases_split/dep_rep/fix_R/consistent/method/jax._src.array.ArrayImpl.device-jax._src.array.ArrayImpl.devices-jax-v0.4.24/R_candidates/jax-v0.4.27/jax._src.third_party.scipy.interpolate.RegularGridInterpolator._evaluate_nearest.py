  def _evaluate_nearest(self, indices, norm_distances):
    idx_res = [
        where(yi <= .5, i, i + 1) for i, yi in zip(indices, norm_distances)
    ]
    return self.values[tuple(idx_res)]
