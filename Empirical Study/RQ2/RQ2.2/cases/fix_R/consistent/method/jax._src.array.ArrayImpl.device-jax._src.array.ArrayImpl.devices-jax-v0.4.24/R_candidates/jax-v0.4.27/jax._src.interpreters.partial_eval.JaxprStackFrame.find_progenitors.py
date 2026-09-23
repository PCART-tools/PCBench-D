  def find_progenitors(self, tracer):
    var = self.tracer_to_var.get(id(tracer))
    if not var:
      return None, None
    active_vars = {var}
    for eqn in self.eqns[::-1]:
      produced = set(eqn.outvars) & active_vars
      if produced:
        active_vars.difference_update(produced)
        active_vars.update(eqn.invars)
    invar_positions = [i for i, v in enumerate(self.invars) if v in active_vars]
    constvars = active_vars & set(self.constvar_to_val)
    const_eqns = [eqn for eqn in self.eqns if set(eqn.invars) & constvars]
    return invar_positions, const_eqns
