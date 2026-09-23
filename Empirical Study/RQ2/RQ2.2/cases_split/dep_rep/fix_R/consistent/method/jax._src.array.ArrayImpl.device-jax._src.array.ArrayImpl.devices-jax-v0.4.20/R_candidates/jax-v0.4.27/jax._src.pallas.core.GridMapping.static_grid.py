  @property
  def static_grid(self) -> StaticGrid:
    if self.num_dynamic_grid_bounds:
      raise ValueError("Expected a grid with fully static bounds")
    return self.grid  # typing: ignore
