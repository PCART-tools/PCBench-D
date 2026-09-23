def get_if_single_primitive(fun: Callable[..., Any], *args: Any) -> jax.core.Primitive | None:
  """
  If fun(*args) lowers to a single primitive with inputs and outputs matching
  function inputs and outputs, return that primitive. Otherwise return None.
  """
  try:
    jaxpr = jax.make_jaxpr(fun)(*args)
  except:
    return None
  while len(jaxpr.eqns) == 1:
    eqn = jaxpr.eqns[0]
    if (eqn.invars, eqn.outvars) != (jaxpr.jaxpr.invars, jaxpr.jaxpr.outvars):
      return None
    elif (eqn.primitive == jax._src.pjit.pjit_p and
          all(jax._src.pjit.is_unspecified(sharding) for sharding in
              (*eqn.params['in_shardings'], *eqn.params['out_shardings']))):
      jaxpr = jaxpr.eqns[0].params['jaxpr']
    else:
      return jaxpr.eqns[0].primitive
  return None
