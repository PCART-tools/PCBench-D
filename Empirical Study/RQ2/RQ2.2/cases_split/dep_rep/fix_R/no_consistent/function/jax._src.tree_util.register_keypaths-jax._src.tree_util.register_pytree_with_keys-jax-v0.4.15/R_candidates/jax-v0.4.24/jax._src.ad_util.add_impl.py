@add_jaxvals_p.def_impl
def add_impl(x, y):
  return raw_jaxval_adders[type(x)](x, y)
