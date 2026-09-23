  def post_process_map(self, primitive, out_tracers, params):
    unknown_out_tracers = [t for t in out_tracers if not t.is_known()]
    jaxpr, res, env = tracers_to_jaxpr([], unknown_out_tracers)
    out_pvals = [t.pval for t in out_tracers]
    out_knowns, out_avals_mapped, out_consts = partition_pvals(out_pvals)
    out = [*out_consts, *res]
    main = self.main

    with core.extend_axis_env(params['axis_name'], params['axis_size'], None):
      call_jaxpr = convert_constvars_jaxpr(jaxpr)

    def todo(out):
      trace = main.with_cur_sublevel()
      out_consts, res = split_list(out, [len(out) - len(jaxpr.constvars)])
      const_tracers = map(trace.new_instantiated_const, res)
      env_tracers = map(trace.full_raise, env)

      staged_out_axes = tuple(out_axes_unknown)  # set by out_axes_transform
      staged_in_axes = (0,) * len(res) + (None,) * len(env)

      update_params = call_param_updaters.get(primitive) or (lambda p, _, __: p)
      staged_params = update_params(params, [], len(res) + len(env))
      staged_params = dict(staged_params, in_axes=staged_in_axes,
                           out_axes=tuple(staged_out_axes),
                           call_jaxpr=call_jaxpr)

      out_avals = [unmapped_aval(params['axis_size'], params['axis_name'], d, a)
                   for d, a in zip(staged_out_axes, out_avals_mapped)]
      out_tracers = [JaxprTracer(trace, PartialVal.unknown(a), None)
                     for a in out_avals]
      name_stack = self._current_truncated_name_stack()
      source = source_info_util.current().replace(name_stack=name_stack)
      eqn = new_eqn_recipe((*const_tracers, *env_tracers), out_tracers,
                           primitive, staged_params, jaxpr.effects, source)
      for t in out_tracers: t.recipe = eqn
      return merge_lists(out_knowns, out_tracers, out_consts)

    def out_axes_transform(out_axes):
      nonlocal out_axes_unknown
      out_axes_unknown, out_axes_known = partition_list(out_knowns, out_axes)
      return tuple(out_axes_known) + (0,) * len(jaxpr.constvars)
    out_axes_unknown: list | None = None

    return out, (todo, out_axes_transform)
