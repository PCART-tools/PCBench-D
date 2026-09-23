  def process_custom_vjp_call(self, prim, f, fwd, bwd, tracers, out_trees,
                              symbolic_zeros):
    # TODO(mattjj): after old remat is deleted, make this method trivial.
    # Because we instantiate all tracers, in_knowns is all False.
    tracers = map(self.instantiate_const_abstracted, tracers)
    in_knowns, in_avals, () = partition_pvals([t.pval for t in tracers])
    f = trace_to_subjaxpr_nounits(f, self.main, True)
    f, aux = partial_eval_wrapper_nounits(f, tuple(in_knowns), tuple(in_avals))
    out_flat = prim.bind(f, fwd, bwd, out_trees=out_trees,
                         symbolic_zeros=symbolic_zeros)
    out_knowns, out_avals, jaxpr, env = aux()
    out_consts, res = split_list(out_flat, [len(out_flat)-len(jaxpr.constvars)])
    res_tracers = map(self.new_instantiated_const, res)
    env_tracers = map(self.full_raise, env)
    out_tracers = [JaxprTracer(self, PartialVal.unknown(a), None)
                   for a in out_avals]
    closed_jaxpr = core.ClosedJaxpr(convert_constvars_jaxpr(jaxpr), ())

    @_memoize
    def fwd_jaxpr_thunk(*zeros):
      fwd_ = _interleave_fun(fwd, zeros)
      fwd_ = trace_to_subjaxpr_nounits(fwd_, self.main, True)
      fwd_, aux = partial_eval_wrapper_nounits(
          fwd_, tuple(in_knowns), tuple(in_avals))
      with core.new_sublevel():
        out_flat = fwd_.call_wrapped()
      out_knowns, out_avals, jaxpr, env = aux()
      _, res = split_list(out_flat, [len(out_flat)-len(jaxpr.constvars)])
      converted_jaxpr = convert_envvars_to_constvars(jaxpr, len(env))
      return converted_jaxpr, (*res, *env)

    name_stack = self._current_truncated_name_stack()
    source = source_info_util.current().replace(name_stack=name_stack)
    eqn = new_eqn_recipe((*res_tracers, *env_tracers, *tracers),
                         out_tracers, prim.initial_style,
                         dict(fun_jaxpr=closed_jaxpr,
                              fwd_jaxpr_thunk=fwd_jaxpr_thunk,
                              num_consts=len(res) + len(env),
                              bwd=bwd, out_trees=out_trees,
                              symbolic_zeros=symbolic_zeros),
                         jaxpr.effects, source)
    for t in out_tracers: t.recipe = eqn
    return merge_lists(out_knowns, out_tracers, out_consts)
