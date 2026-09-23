def ignore_error_output_jaxpr(jaxpr):
  """Constructs a checked jaxpr which does not output its error value."""
  consts = jaxpr.consts
  jaxpr = jaxpr.jaxpr
  new_jaxpr = jaxpr.replace(outvars=jaxpr.outvars[3:])
  return core.ClosedJaxpr(new_jaxpr, consts)
