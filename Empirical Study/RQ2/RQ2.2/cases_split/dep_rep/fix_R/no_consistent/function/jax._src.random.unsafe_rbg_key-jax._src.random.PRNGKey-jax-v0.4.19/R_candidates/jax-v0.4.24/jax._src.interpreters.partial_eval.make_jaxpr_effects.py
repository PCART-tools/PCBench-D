def make_jaxpr_effects(constvars, invars, outvars, eqns) -> effects.Effects:
  jaxpr_effects = set()
  all_vars = [*constvars, *invars]
  for eqn in eqns:
    for eff in eqn.effects:
      if isinstance(eff, effects.JaxprInputEffect):
        if eff.input_index >= len(eqn.invars):
          raise ValueError(
              f"`JaxprInputEffect` {eff} is invalid."
              f"\n Equation: {eqn}\n"
              "\n Jaxpr: "
              f"{core.Jaxpr(constvars, invars, outvars, eqns, set())}")
        invar = eqn.invars[eff.input_index]
        if invar not in all_vars:
          raise ValueError(
                f"`JaxprInputEffect` {eff} does not have "
                f"corresponding input: {invar}."
                f"\n Equation: {eqn}\n"
                "\n Jaxpr: "
                f"{core.Jaxpr(constvars, invars, outvars, eqns, set())}")
        eff = eff.replace(input_index=all_vars.index(invar))
      jaxpr_effects.add(eff)
  return jaxpr_effects
