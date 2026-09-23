@add_jaxvals_p.def_abstract_eval
def add_abstract(xs, ys):
  return lattice_join(xs, ys)
