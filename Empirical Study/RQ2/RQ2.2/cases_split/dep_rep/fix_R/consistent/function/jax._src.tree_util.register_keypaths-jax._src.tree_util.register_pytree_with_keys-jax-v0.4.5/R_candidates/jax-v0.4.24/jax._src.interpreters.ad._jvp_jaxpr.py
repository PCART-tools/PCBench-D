@weakref_lru_cache
def _jvp_jaxpr(jaxpr, nonzeros, instantiate):
  assert len(jaxpr.in_avals) == len(nonzeros)
  f = lu.wrap_init(core.jaxpr_as_fun(jaxpr))
  f_jvp, out_nonzeros = f_jvp_traceable(jvp(f, instantiate=instantiate, transform_stack=False),
                                        nonzeros)
  tangent_avals = [aval for aval, nz in zip(jaxpr.in_avals, nonzeros) if nz]
  avals_in = list(it.chain(jaxpr.in_avals, tangent_avals))
  jaxpr_out, avals_out, literals_out, () = pe.trace_to_jaxpr_dynamic(f_jvp, avals_in)
  return core.ClosedJaxpr(jaxpr_out, literals_out), out_nonzeros()
