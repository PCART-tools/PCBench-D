  @functools.cached_property
  def has_communication(self) -> bool:
    return bool(jax_core.used_axis_names_jaxpr(self.jaxpr))
