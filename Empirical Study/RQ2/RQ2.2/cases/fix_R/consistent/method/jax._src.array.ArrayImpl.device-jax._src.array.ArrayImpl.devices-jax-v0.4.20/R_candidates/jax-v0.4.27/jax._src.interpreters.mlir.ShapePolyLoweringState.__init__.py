  def __init__(self,
               dim_vars: tuple[str, ...],
               lowering_platforms: tuple[str, ...] | None):
    if lowering_platforms is not None and len(lowering_platforms) > 1:
      dim_vars = ("_platform_index",) + tuple(dim_vars)
      self.has_platform_index_argument = True
    else:
      self.has_platform_index_argument = False
    self.uses_dim_vars = (len(dim_vars) > 0)
    self.dim_vars = dim_vars
