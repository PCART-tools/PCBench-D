def _partial_eval_jaxpr_custom(jaxpr, in_unknowns, policy):
  # A simple wrapper around `pe.partial_eval_jaxpr_custom` that assumes all
  # inputs are instantiated and doesn't ensure any outputs are unknown or
  # instantiated.
  return pe.partial_eval_jaxpr_custom(
      jaxpr, in_unknowns, [True] * len(in_unknowns), False, False, policy)
