@cache()
def _reduction_jaxpr(computation, aval):
  @lu.wrap_init
  def comp(x, y):
    result = computation(x, y)
    if not (isinstance(result, core.Tracer) or core.valid_jaxtype(result)):
      raise ValueError(
          f"Invalid return type from reduction function: {type(result)}\n"
          f"Reduction functions should only return an array.\n"
          f"Full return value: {result}")
    return (result,)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(comp, (aval, aval))
  if any(isinstance(c, core.Tracer) for c in consts):
    raise NotImplementedError(
        "Reduction computations can't close over Tracers. Please open an issue "
        "at https://github.com/google/jax.")
  return jaxpr, tuple(consts)
