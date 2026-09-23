  def replace(
      self,
      invars: list[Atom] | None = None,
      outvars: list[Var] | None = None,
      primitive: Primitive | None = None,
      params: dict[str, Any] | None = None,
      effects: Effects | None = None,
      source_info: source_info_util.SourceInfo | None = None,
  ):
    # It is slightly faster to rebuild the tuple directly than to call _replace.
    return JaxprEqn(
      self.invars if invars is None else invars,
      self.outvars if outvars is None else outvars,
      self.primitive if primitive is None else primitive,
      self.params if params is None else params,
      self.effects if effects is None else effects,
      self.source_info if source_info is None else source_info,
    )
