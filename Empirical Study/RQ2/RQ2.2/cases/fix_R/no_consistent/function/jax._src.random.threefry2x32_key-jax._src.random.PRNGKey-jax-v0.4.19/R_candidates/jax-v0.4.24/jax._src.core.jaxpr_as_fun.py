@curry
def jaxpr_as_fun(closed_jaxpr: ClosedJaxpr, *args):
  return eval_jaxpr(closed_jaxpr.jaxpr, closed_jaxpr.consts, *args)
