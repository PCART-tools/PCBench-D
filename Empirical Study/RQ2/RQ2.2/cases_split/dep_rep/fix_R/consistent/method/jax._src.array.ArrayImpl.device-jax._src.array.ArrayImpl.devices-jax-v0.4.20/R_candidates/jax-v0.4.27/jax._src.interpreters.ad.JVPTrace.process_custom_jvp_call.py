  def process_custom_jvp_call(self, _, __, f_jvp, tracers, *, symbolic_zeros):
    primals_in, tangents_in = unzip2((t.primal, t.tangent) for t in tracers)
    primals_in = map(core.full_lower, primals_in)
    if not symbolic_zeros:
      tangents_in = map(instantiate_zeros, tangents_in)
      tangents_in = map(replace_float0s, primals_in, tangents_in)
    else:
      tangents_in = map(replace_internal_symbolic_zeros, tangents_in)
    outs = f_jvp.call_wrapped(*it.chain(primals_in, tangents_in))
    primals_out, tangents_out = split_list(outs, [len(outs) // 2])
    tangents_out = map(replace_rule_output_symbolic_zeros, tangents_out)
    tangents_out = map(recast_to_float0, primals_out, tangents_out)
    return map(partial(JVPTracer, self), primals_out, tangents_out)
