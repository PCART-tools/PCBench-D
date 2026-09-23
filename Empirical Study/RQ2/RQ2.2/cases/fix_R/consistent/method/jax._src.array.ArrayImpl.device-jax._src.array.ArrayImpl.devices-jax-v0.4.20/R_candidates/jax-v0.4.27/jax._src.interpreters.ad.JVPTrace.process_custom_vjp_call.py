  def process_custom_vjp_call(self, _, __, fwd, bwd, tracers, out_trees,
                              symbolic_zeros):
    primals_in, tangents_in = unzip2((t.primal, t.tangent) for t in tracers)
    fwd_in = [(core.full_lower(p), type(t) is not Zero)
              for p, t in zip(primals_in, tangents_in)]
    fwd_in = [x for pair in fwd_in for x in pair]   # flatten
    res_and_primals_out = fwd.call_wrapped(*fwd_in)
    _, res_tree = out_trees()
    res, primals_out = split_list(res_and_primals_out, [res_tree.num_leaves])
    avals_out = [raise_to_shaped(core.get_aval(x)) for x in primals_out]
    # TODO(frostig,mattjj): avoid instantiating zeros when we don't have to!
    tangents_in = map(instantiate_zeros, tangents_in)
    tangents_out = custom_lin_p.bind(
        *res, *tangents_in, num_res=res_tree.num_leaves, bwd=bwd,
        out_avals=avals_out, symbolic_zeros=symbolic_zeros)
    tangents_out = map(jax._src.lax.lax.tie_p.bind, primals_out, tangents_out)
    tangents_out = map(recast_to_float0, primals_out, tangents_out)
    return map(partial(JVPTracer, self), primals_out, tangents_out)
