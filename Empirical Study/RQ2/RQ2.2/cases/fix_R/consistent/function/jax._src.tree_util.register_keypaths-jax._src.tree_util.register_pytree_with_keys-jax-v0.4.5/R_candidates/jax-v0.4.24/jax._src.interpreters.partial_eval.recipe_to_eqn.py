def recipe_to_eqn(getvar: Callable[[JaxprTracer], Atom],
                  recipe: JaxprEqnRecipe) -> core.JaxprEqn:
  (_, in_tracers, out_tracer_refs, out_avals, prim, params, eff, src) = recipe
  invars  = [getvar(t) for t in in_tracers]
  out_tracers = [t_ref() for t_ref in out_tracer_refs]
  outvars = [DropVar(a) if t is None else getvar(t)  # type: ignore
             for a, t in zip(out_avals, out_tracers)]
  return new_jaxpr_eqn(invars, outvars, prim, params, eff, src)
