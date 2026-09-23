  def process_call(self, primitive, f, tracers, params):
    rule = call_partial_eval_rules.get(primitive)
    if rule:
      return rule(self, primitive, f, tracers, params)

    update_params = call_param_updaters.get(primitive) or (lambda p, _, __: p)
    in_knowns, in_avals, in_consts = partition_pvals([t.pval for t in tracers])
    # TODO(mattjj): check in_avals are consistent with f.in_type

    # We want to partially evaluate this call into two calls: one evaluated now
    # taking known values (in_consts) as inputs and producing known values
    # (out_consts) as outputs, and the other staged out as an eqn into the jaxpr
    # being built. The latter takes as input residuals (res) produced as outputs
    # of the first call, shared closed-over values (env), and explicit arguments
    # which were unknown to the first call (corresponding to in_avals).

    # Wrap f to perform the partial evaluation and plumb out aux data.
    if not config.dynamic_shapes.value:
      f_ = trace_to_subjaxpr_nounits_fwd(f, self.main, False)
      f_, aux = partial_eval_wrapper_nounits(f_, tuple(in_knowns),
                                             tuple(in_avals))
    else:
      if f.in_type is None:
        f = lu.annotate(f, tuple((a, True) for a in in_avals))
      f_, aux = trace_to_subjaxpr_nounits_dyn(f, self.main, tuple(in_knowns),
                                              f.in_type, False)
    # Adjust parameters (e.g. donated_invars) for the call to be evaluated now.
    const_params = update_params(params, in_knowns, 0)

    # Run the call, getting known out vals and aux data used for staged-out call
    out = primitive.bind(_update_annotation_known(f_, f.in_type, in_knowns),
                         *in_consts, **const_params)
    fwds, out_knowns, out_type, jaxpr, env = aux()
    # Split apart known outputs from the original call and non-fwded residuals.
    out_consts, non_fwd_res = split_list(out, [sum(out_knowns)])

    # Form the complete list of residuals by forwarding some inputs.
    if config.dynamic_shapes.value:
      # With dynamic shapes, we may need to forward implicit arguments.
      in_consts_, in_knowns_ = iter(in_consts), iter(in_knowns)
      in_consts_full = [None] * len(f.in_type)
      for idx, (aval, explicit) in enumerate(f.in_type):
        if explicit and next(in_knowns_):
          c = in_consts_full[idx] = next(in_consts_)
          if aval.shape:
            for d1, d2 in zip(aval.shape, c.shape):
              if type(d1) is DBIdx:
                in_consts_full[d1.val] = d2
    else:
      in_consts_full = in_consts
    res = subs_list(fwds, in_consts_full, non_fwd_res)

    # Create the input tracers for the staged-out (unknown-value) call.
    res_tracers = map(self.instantiate_const, map(self.new_const, res))
    env_tracers = map(self.full_raise, env)
    unknown_arg_tracers = [t for t in tracers if not t.is_known()]
    # Adjust parameters (e.g. donated_invars) for the staged-out call's args.
    num_new_args = len(res_tracers) + len(env_tracers)
    staged_params = dict(params, call_jaxpr=convert_constvars_jaxpr(jaxpr))
    staged_params = update_params(staged_params, map(op.not_, in_knowns),
                                  num_new_args)
    # The outputs of the staged-out call are Tracers with the new eqn as recipe.
    if config.dynamic_shapes.value:
      # With dynamic shapes, we may need to substitute Tracers into avals.
      out_tracers = []
      for aval, _ in out_type:
        assert not isinstance(aval, ConcreteArray)
        if type(aval) is DShapedArray:
          shape = [[*res_tracers, *env_tracers, *unknown_arg_tracers][d.val]
                  if type(d) is InDBIdx else d for d in aval.shape]
          aval = aval.update(shape=tuple(shape))
        out_tracers.append(JaxprTracer(self, PartialVal.unknown(aval), None))
    else:
      out_tracers = [JaxprTracer(self, PartialVal.unknown(a), None)
                     for a in out_type]
    name_stack = self._current_truncated_name_stack()
    source = source_info_util.current().replace(name_stack=name_stack)
    eqn = new_eqn_recipe((*res_tracers, *env_tracers, *unknown_arg_tracers),
                         out_tracers, primitive, staged_params, jaxpr.effects,
                         source)
    for t in out_tracers: t.recipe = eqn
    return merge_lists(out_knowns, out_tracers, out_consts)
