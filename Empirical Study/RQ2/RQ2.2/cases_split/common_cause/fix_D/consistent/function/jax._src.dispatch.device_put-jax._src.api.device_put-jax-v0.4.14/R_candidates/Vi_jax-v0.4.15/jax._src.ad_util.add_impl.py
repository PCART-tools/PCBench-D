@add_jaxvals_p.def_impl
def add_impl(xs, ys):
  return jaxval_adders[type(xs)](xs, ys)
