  def process_custom_transpose(self, prim, call, tracers, **params):
    res_ts, lin_ts = split_list(tracers, [params['res_tree'].num_leaves])
    assert all(t.is_known()     for t in res_ts)
    lin_all_known   = all(t.is_known()     for t in lin_ts)
    if lin_all_known:
      res_cvals = [t.pval[1] for t in res_ts]
      lin_cvals = [t.pval[1] for t in lin_ts]
      return prim.bind(call, *res_cvals, *lin_cvals, **params)
    else:
      out_tracers = [JaxprTracer(self, PartialVal.unknown(aval), None)
                     for aval in params['out_types']]
      in_tracers = map(self.instantiate_const, tracers)
      new_params = dict(params, call=call)
      eqn = new_eqn_recipe(in_tracers, out_tracers, prim, new_params,
          core.no_effects, source_info_util.current())
      for t in out_tracers: t.recipe = eqn
      return out_tracers
