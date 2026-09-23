  def post_process_call(self, primitive, out_tracers, params):
    unknown_out_tracers = [t for t in out_tracers if not t.is_known()]
    jaxpr, res, env = tracers_to_jaxpr([], unknown_out_tracers)
    out_pvals = [t.pval for t in out_tracers]
    out_knowns, out_avals, out_consts = partition_pvals(out_pvals)
    out = [*out_consts, *res]
    main = self.main

    def todo(out):
      trace = main.with_cur_sublevel()
      out_consts, res = split_list(out, [len(out) - len(jaxpr.constvars)])
      const_tracers = map(trace.new_instantiated_const, res)
      in_tracers = (*const_tracers, *map(trace.full_raise, env))
      out_tracers = [JaxprTracer(trace, PartialVal.unknown(a), None)
                     for a in out_avals]
      update_params = call_param_updaters.get(primitive) or (lambda p, _, __: p)
      new_params = update_params(params, [], len(in_tracers))
      new_params = dict(new_params, call_jaxpr=convert_constvars_jaxpr(jaxpr))
      name_stack = self._current_truncated_name_stack()
      source = source_info_util.current().replace(name_stack=name_stack)
      eqn = new_eqn_recipe(in_tracers, out_tracers, primitive, new_params,
          jaxpr.effects, source)
      for t in out_tracers: t.recipe = eqn
      return merge_lists(out_knowns, out_tracers, out_consts)

    return out, todo
