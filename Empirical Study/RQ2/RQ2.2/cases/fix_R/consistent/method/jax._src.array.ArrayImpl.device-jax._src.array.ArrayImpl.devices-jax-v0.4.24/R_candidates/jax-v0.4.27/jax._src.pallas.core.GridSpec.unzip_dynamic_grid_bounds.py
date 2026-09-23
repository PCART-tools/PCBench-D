  def unzip_dynamic_grid_bounds(self) -> tuple[GridSpec, tuple[Any, ...]]:
    static_grid = tuple(d if isinstance(d, int) else None for d in self.grid)
    dynamic_bounds = tuple(d for d in self.grid if not isinstance(d, int))
    # We can't use dataclasses.replace, because our fields are incompatible
    # with __init__'s signature.
    static_self = copy.copy(self)
    static_self.grid = static_grid
    return static_self, dynamic_bounds
