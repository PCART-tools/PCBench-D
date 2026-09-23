@add_jaxvals_p.def_abstract_eval
def add_abstract(x, y):
  return core.lattice_join(x, y)
