@dataclasses.dataclass(frozen=True)
class GridMapping:
  grid: Grid
  block_mappings: tuple[BlockMapping | None, ...]
  mapped_dims: tuple[int, ...]
  num_index_operands: int
  num_scratch_operands: int

  replace = dataclasses.replace

  @property
  def num_dynamic_grid_bounds(self):
    return sum(b is None for b in self.grid)

  @property
  def static_grid(self) -> StaticGrid:
    if self.num_dynamic_grid_bounds:
      raise ValueError("Expected a grid with fully static bounds")
    return self.grid  # typing: ignore
