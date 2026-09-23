class JaxprTrace(Trace['JaxprTracer']):

  def __init__(self, *args, name_stack: source_info_util.NameStack):
    super().__init__(*args)
    self.name_stack = name_stack

  def pure(self, val: Any) -> JaxprTracer:
    return self.new_const(val)

  def lift(self, val: Tracer) -> JaxprTracer:
    return self.new_const(val)

  def sublift(self, val: JaxprTracer) -> JaxprTracer:
    return JaxprTracer(self, val.pval, FreeVar(val))

  def new_const(self, val) -> JaxprTracer:
    if isinstance(val, Tracer) and val._trace.level == self.level:
      raise Exception
    return JaxprTracer(self, PartialVal.known(val), None)

  def new_instantiated_literal(self, val) -> JaxprTracer:
    aval = get_aval(val)
    return JaxprTracer(self, PartialVal.unknown(aval),
                       Literal(val, raise_to_shaped(aval)))

  def new_instantiated_const(self, val) -> JaxprTracer:
    aval = get_aval(val)
    if isinstance(aval, DShapedArray):
      shape = [self.new_instantiated_const(d)
               if isinstance(d, Tracer) and d._trace.level < self.level else d
               for d in aval.shape]
      aval = aval.update(shape=tuple(shape))
    return JaxprTracer(self, PartialVal.unknown(aval), ConstVar(val))

  def new_arg(self, pval: PartialVal) -> JaxprTracer:
    const = pval.get_known()
    # XXX: Think twice before changing this constant argument pruning!
    # This has really important consequences for partial_eval_jaxpr.
    # Most importantly, this guarantees that the unknown jaxpr never uses
    # known inputs (if it needs them, then they get passed through residuals).
    if const is None:
      aval = pval.get_aval()
      if type(aval) is DShapedArray:
        shape = [self.new_instantiated_const(d)
                 if isinstance(d, Tracer) and d._trace.level < self.level else d
                 for d in aval.shape]
        aval = aval.update(shape=tuple(shape))
      return JaxprTracer(self, PartialVal.unknown(aval), LambdaBinding())
    else:
      return self.new_const(const)

  def instantiate_const(self, tracer: JaxprTracer) -> JaxprTracer:
    const = tracer.pval.get_known()
    if const is None:
      return tracer
    else:
      if type(const) in core.literalable_types and np.shape(const) == ():
        return self.new_instantiated_literal(const)
      else:
        return self.new_instantiated_const(const)

  def instantiate_const_abstracted(self, tracer) -> JaxprTracer:
    const = tracer.pval.get_known()
    if const is None:
      return tracer
    else:
      aval = raise_to_shaped(get_aval(const), np.isscalar(const))
      return JaxprTracer(self, PartialVal.unknown(aval), ConstVar(const))

  def process_primitive(self, primitive, tracers, params):
    if primitive in custom_partial_eval_rules:
      return custom_partial_eval_rules[primitive](self, *tracers, **params)
    else:
      return self.default_process_primitive(primitive, tracers, params)

  def default_process_primitive(self, primitive, tracers, params):
    # By default, if all the input tracers are known, then bind the primitive
    # and consider all outputs known. Otherwise, stage the application into the
    # jaxpr and consider all outputs unknown.
    consts = [t.pval.get_known() for t in tracers]
    if all(c is not None for c in consts):
      return primitive.bind(*consts, **params)
    tracers = map(self.instantiate_const, tracers)
    avals = [t.aval for t in tracers]
    out_aval, effects = primitive.abstract_eval(*avals, **params)
    name_stack = self._current_truncated_name_stack()
    source = source_info_util.current().replace(name_stack=name_stack)
    if primitive.multiple_results:
      out_tracers = [JaxprTracer(self, PartialVal.unknown(aval), None)
                     for aval in out_aval]
      eqn = new_eqn_recipe(tracers, out_tracers, primitive, params, effects, source)
      for t in out_tracers: t.recipe = eqn
      return out_tracers
    else:
      out_tracer = JaxprTracer(self, PartialVal.unknown(out_aval), None)
      out_tracer.recipe = new_eqn_recipe(tracers, [out_tracer], primitive,
                                         params, effects, source)
      return out_tracer

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

  def process_map(self, primitive, f: lu.WrappedFun, tracers, params):
    update_params = call_param_updaters.get(primitive) or (lambda p, _, __: p)
    in_knowns, in_avals, in_consts = partition_pvals([t.pval for t in tracers])

    # This method is like process_call above, except:
    #   1. we delete an axis from mapped-over input avals' shapes, and
    #      analogously add an axis to mapped-over output avals' shapes;
    #   2. we update the in_axes and out_axes/out_axes_thunk parameters to
    #      reflect the inputs and outputs pruned from the unknown/known sides.

    # Map (delete an axis from) unknown inputs' avals as dictated by in_axes.
    unk_in_axes, const_in_axes = partition_list(in_knowns, params['in_axes'])
    in_avals_mapped = [mapped_aval(params['axis_size'], ax, aval)
                       for ax, aval in zip(unk_in_axes, in_avals)]

    # Wrap f to perform partial evaluation and plumb out aux data.
    f = trace_to_subjaxpr_nounits(f, self.main, False)
    f, aux = partial_eval_wrapper_nounits(f, tuple(in_knowns),
                                          tuple(in_avals_mapped))
    # Adjust params for knowns (e.g. donated_invars, in_axes, out_axes_thunk)
    const_params = update_params(params, in_knowns, 0)  # handles donated_invars
    out_axes_thunk = params['out_axes_thunk']
    @as_hashable_function(closure=out_axes_thunk)
    def const_out_axes_thunk():
      out_knowns, _, jaxpr, _ = aux()
      _, out_axes = partition_list(out_knowns, out_axes_thunk())
      return tuple(out_axes) + (0,) * len(jaxpr.constvars)  # res mapped axis 0
    const_params = dict(const_params, in_axes=tuple(const_in_axes),
                        out_axes_thunk=const_out_axes_thunk)

    # Run the map, getting known out vals and aux data used for staged-out map.
    out = primitive.bind(f, *in_consts, **const_params)
    out_knowns, out_avals_mapped, jaxpr, env = aux()
    # Split apart known outputs from the original call and residuals.
    out_consts, res = split_list(out, [len(out) - len(jaxpr.constvars)])

    # We can only check_jaxpr with the dynamic axis environment extended:
    with core.extend_axis_env(params['axis_name'], params['axis_size'], None):
      call_jaxpr = convert_constvars_jaxpr(jaxpr)

    # Compute staged and const out_axes, taking into account residuals.
    out_axes = params['out_axes_thunk']()
    staged_out_axes, _ = partition_list(out_knowns, out_axes)
    staged_in_axes = (0,) * len(res) + (None,) * len(env) + (*unk_in_axes,)

    # Create the input tracers for the staged-out (unkonwn-value) call.
    const_tracers = map(self.new_instantiated_const, res)
    env_tracers = map(self.full_raise, env)
    unknown_arg_tracers = [t for t in tracers if not t.is_known()]
    # Adjust params for staged-out call on unknown values.
    num_new_args = len(const_tracers) + len(env_tracers)
    staged_params = update_params(params, map(op.not_, in_knowns), num_new_args)
    staged_params = dict(staged_params, in_axes=staged_in_axes,
                         out_axes=tuple(staged_out_axes), call_jaxpr=call_jaxpr)
    del staged_params['out_axes_thunk']
    # The outputs of the staged-out call are Tracers with the new eqn as recipe.
    out_avals = [unmapped_aval(params['axis_size'], params['axis_name'], ax, a)
                 for ax, a in zip(staged_out_axes, out_avals_mapped)]
    out_tracers = [JaxprTracer(self, PartialVal.unknown(a), None)
                   for a in out_avals]
    eqn = new_eqn_recipe((*const_tracers, *env_tracers, *unknown_arg_tracers),  # type: ignore[arg-type]
                         out_tracers, primitive, staged_params,
                         jaxpr.effects,
                         source_info_util.current())
    for t in out_tracers: t.recipe = eqn

    return merge_lists(out_knowns, out_tracers, out_consts)

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

  def _current_truncated_name_stack(self):
    return source_info_util.current_name_stack()[len(self.name_stack):]

  def process_custom_jvp_call(self, prim, fun, jvp, tracers, *, symbolic_zeros):
    # We assume partial evaluation is only performed to build linear functions,
    # and hence we don't need to keep the custom JVP rule around anymore.
    del jvp, symbolic_zeros
    assert not all(t.is_known() for t in tracers)
    return fun.call_wrapped(*tracers)

  def post_process_custom_jvp_call(self, out_tracers, _):
    # This path should only be reachable if we expose a partial eval API
    # unrelated to autodiff, since we raise an error when differentiation with
    # respect to values over which a custom_jvp function closes is detected.
    raise NotImplementedError  # TODO(mattjj)

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

  def post_process_custom_vjp_call(self, out_tracers, _):
    # This path should only be reachable if we expose a partial eval API
    # unrelated to autodiff, since we raise an error when differentiation with
    # respect to values over which a custom_vjp function closes is detected.
    raise NotImplementedError  # TODO(mattjj)
