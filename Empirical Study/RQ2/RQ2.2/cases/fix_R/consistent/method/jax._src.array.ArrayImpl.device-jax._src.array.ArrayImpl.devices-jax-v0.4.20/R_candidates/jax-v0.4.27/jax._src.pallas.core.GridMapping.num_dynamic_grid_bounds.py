  @property
  def num_dynamic_grid_bounds(self):
    return sum(b is None for b in self.grid)
