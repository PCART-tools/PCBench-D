class ShapePolyLoweringState:
  # The names of the dimension variables, sorted by name. This is the order in
  # which they are passed to the IR functions that need them. This is only
  # used for native serialization with polymorphic shapes when
  # --jax_dynamic_shapes is off.
  # TODO: for multi-platform lowering we prepend to the regular dimension
  # variables a fake dimension variable "platform_index_". This is a
  # temporary abuse, taking advantage that for platform index we need the
  # same lowering strategy as for dimension variables: add it as argument to
  # inner functions, and pass the values along at the call sites.
  dim_vars: tuple[str, ...]
  # Whether the module uses dimension variables, either in its inputs or
  # from an inner call to Exported modules that uses dimension variables.
  # This includes the case when the called Exported module uses a platform
  # index argument.
  uses_dim_vars: bool

  # If the first dimension variable is a platform index argument
  has_platform_index_argument: bool

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
