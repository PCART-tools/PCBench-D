  def replace(self, **kwargs):
    jaxpr = Jaxpr(
        constvars=kwargs.pop("constvars", self.constvars),
        invars=kwargs.pop("invars", self.invars),
        outvars=kwargs.pop("outvars", self.outvars),
        eqns=kwargs.pop("eqns", self.eqns),
        effects=kwargs.pop("effects", self.effects),
        debug_info=kwargs.pop("debug_info", self.debug_info),
    )
    if kwargs:
      raise ValueError(f"Unknown keyword arguments: {kwargs}")
    return jaxpr
