@remat_p.def_effectful_abstract_eval
def remat_abstract_eval(*args, jaxpr, prevent_cse, differentiated, policy):
  del args, prevent_cse, differentiated, policy  # Unused.
  return [v.aval for v in jaxpr.outvars], jaxpr.effects
