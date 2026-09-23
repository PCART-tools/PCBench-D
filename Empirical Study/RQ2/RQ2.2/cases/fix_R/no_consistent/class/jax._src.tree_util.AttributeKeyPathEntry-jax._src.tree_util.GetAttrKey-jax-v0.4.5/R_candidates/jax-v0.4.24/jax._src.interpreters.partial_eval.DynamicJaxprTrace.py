class DynamicJaxprTrace(core.Trace):
  __slots__ = []  # type: ignore

  @property
  def frame(self):
    return self.main.jaxpr_stack[-1]  # pytype: disable=attribute-error

  def new_arg(self, aval):
    tracer = DynamicJaxprTracer(self, aval, source_info_util.current())
    self.frame.tracers.append(tracer)
    self.frame.tracer_to_var[id(tracer)] = var = self.frame.newvar(aval)
    self.frame.invars.append(var)
    return tracer

  def new_const(self, c):
    # TODO(mattjj): for ints, or hashable consts, don't rely on id
    tracer = self.frame.constid_to_tracer.get(id(c))
    if tracer is None:
      aval = raise_to_shaped(get_aval(c), weak_type=dtypes.is_weakly_typed(c))
      aval = self._lift_tracers_in_aval(aval)
      tracer = self._new_const(aval, c)
    return tracer

  pure = lift = new_const

  def _new_const(self, aval, c):
    tracer = DynamicJaxprTracer(self, aval, source_info_util.current())
    self.frame.tracers.append(tracer)
    self.frame.tracer_to_var[id(tracer)] = var = self.frame.newvar(aval)
    self.frame.constid_to_tracer[id(c)] = tracer
    self.frame.constvar_to_val[var] = c
    return tracer

  def sublift(self, t):
    # When lifting closed-over tracers corresponding to this same trace, the
    # variable to lift could have tracers (representing axis size variables) in
    # its shape. We must lift those too!
    tracer = self.frame.constid_to_tracer.get(id(t))
    if tracer is None:
      aval = raise_to_shaped(get_aval(t), weak_type=dtypes.is_weakly_typed(t))
      aval = self._lift_tracers_in_aval(aval)
      tracer = self._new_const(aval, t)
    return tracer

  def _lift_tracers_in_aval(self, aval):
    if (not isinstance(aval, DShapedArray) or
        not any(isinstance(d, Tracer) for d in aval.shape)):
      return aval
    shape = [self.full_raise(d) if isinstance(d, Tracer) else d
             for d in aval.shape]
    return aval.update(shape=tuple(shape))

  def getvar(self, tracer):
    var = self.frame.tracer_to_var.get(id(tracer))
    if var is None:
      raise core.escaped_tracer_error(tracer)
    return var

  def makevar(self, tracer):
    var = self.frame.tracer_to_var.get(id(tracer))
    assert var is None, "a jaxpr variable must be created only once per tracer"
    self.frame.tracers.append(tracer)
    var = self.frame.tracer_to_var[id(tracer)] = self.frame.newvar(tracer.aval)
    return var

  def instantiate_const(self, val):
    if (isinstance(val, Tracer) and val._trace.main is self.main
        and val._trace.sublevel == self.sublevel):
      return val
    else:
      return self.new_const(val)

  def process_primitive(self, primitive, tracers, params):
    if primitive in custom_staging_rules:
      return custom_staging_rules[primitive](self, *tracers, **params)
    return self.default_process_primitive(primitive, tracers, params)

  def default_process_primitive(self, primitive, tracers, params):
    avals = [t.aval for t in tracers]
    out_avals, effects = primitive.abstract_eval(*avals, **params)
    # == serve as a "not xor" here.
    if not (isinstance(out_avals, (tuple,list)) == primitive.multiple_results):
      raise ValueError(f"{primitive}.abstract_eval() method should return"
                       f" a tuple or a list if {primitive}.multiple_results"
                       " is true. Otherwise it shouldn't.")
    out_avals = [out_avals] if not primitive.multiple_results else out_avals
    source_info = source_info_util.current()
    out_tracers = [DynamicJaxprTracer(self, a, source_info) for a in out_avals]
    invars = map(self.getvar, tracers)
    outvars = map(self.makevar, out_tracers)
    eqn = new_jaxpr_eqn(invars, outvars, primitive, params, effects, source_info)
    self.frame.add_eqn(eqn)
    return out_tracers if primitive.multiple_results else out_tracers.pop()

  def process_call(self, call_primitive, f, explicit_tracers, params):
    if f.in_type is None:
      f = lu.annotate(f, tuple((raise_to_shaped(t.aval), True)
                               for t in explicit_tracers))
    implicit_tracers = _extract_implicit_args(self, f.in_type, explicit_tracers)
    in_tracers = [*implicit_tracers, *explicit_tracers]
    # TODO(mattjj): check in_tracers are consistent with f.in_type annotation
    with core.new_sublevel():
      # TODO(lenamartens): Make call_primitive name -> API function name mapping.
      # (currently this will display eg. 'xla_call' instead of `jit`)
      dbg = debug_info_final(f, call_primitive.name)
      jaxpr, out_type, consts = trace_to_subjaxpr_dynamic2(f, self.main, debug_info=dbg)
    if params.get('inline', False):
      return core.eval_jaxpr(jaxpr, consts, *in_tracers,
                             propagate_source_info=False)
    source_info = source_info_util.current()
    out_tracers = []
    for aval, _ in out_type:
      if type(aval) is DShapedArray:
        shape = [[*consts, *in_tracers][d.val] if type(d) is InDBIdx else
                 out_tracers[d.val] if type(d) is OutDBIdx else
                 d for d in aval.shape]
        aval = aval.update(shape=tuple(get_referent(d) for d in shape))
      out_tracers.append(DynamicJaxprTracer(self, aval, source_info))
    invars = map(self.getvar, in_tracers)
    constvars = map(self.getvar, map(self.instantiate_const, consts))
    outvars = map(self.makevar, out_tracers)
    new_params = dict(params, call_jaxpr=convert_constvars_jaxpr(jaxpr))
    update_params = call_param_updaters.get(call_primitive)
    if update_params:
      new_params = update_params(new_params, [True] * len(explicit_tracers),
                                 len(consts) + len(implicit_tracers))
    eqn = new_jaxpr_eqn([*constvars, *invars], outvars, call_primitive,
                        new_params, new_params['call_jaxpr'].effects,
                        source_info)
    self.frame.add_eqn(eqn)
    return [t for t, (_, keep) in zip(out_tracers, out_type) if keep]

  def post_process_call(self, call_primitive, out_tracers, params):
    assert False  # unreachable

  def process_map(self, map_primitive, f, tracers, params):
    in_avals = [t.aval for t in tracers]
    axis_name, axis_size = params['axis_name'], params['axis_size']
    reduced_in_avals = [core.mapped_aval(axis_size, in_axis, a)
                        if in_axis is not None else a
                        for a, in_axis in zip(in_avals, params['in_axes'])]
    with core.extend_axis_env(axis_name, params["global_axis_size"], None):  # type: ignore
      with core.new_sublevel():
        jaxpr, reduced_out_avals, consts, () = trace_to_subjaxpr_dynamic(
            f, self.main, reduced_in_avals,
            debug_info=debug_info_final(f, map_primitive.name))
      ordered_effects = effects.ordered_effects.filter_in(jaxpr.effects)
      if ordered_effects:
        raise ValueError("Ordered effects not supported for "
                         f"map primitives: {ordered_effects}")
      out_axes = params['out_axes_thunk']()
      out_avals = [core.unmapped_aval(axis_size, axis_name, out_axis, a)
                  if out_axis is not None else a
                  for a, out_axis in zip(reduced_out_avals, out_axes)]
      source_info = source_info_util.current()
      out_tracers = [DynamicJaxprTracer(self, a, source_info) for a in out_avals]
      invars = map(self.getvar, tracers)
      constvars = map(self.getvar, map(self.instantiate_const, consts))
      outvars = map(self.makevar, out_tracers)
      new_in_axes = (None,) * len(consts) + params['in_axes']
      new_params = dict(params, in_axes=new_in_axes, out_axes=out_axes,
                        call_jaxpr=convert_constvars_jaxpr(jaxpr))
      del new_params['out_axes_thunk']
      update_params = call_param_updaters.get(map_primitive)
      if update_params:
        new_params = update_params(new_params, [True] * len(tracers), len(consts))
      eqn = new_jaxpr_eqn([*constvars, *invars], outvars, map_primitive,
                          new_params, jaxpr.effects, source_info)
      self.frame.add_eqn(eqn)
    return out_tracers

  def post_process_map(self, map_primitive, out_tracers, params):
    assert False  # unreachable

  def process_custom_jvp_call(self, prim, fun, jvp, tracers, *, symbolic_zeros):
    in_avals = [t.aval for t in tracers]
    with core.new_sublevel():
      fun_jaxpr, out_avals, consts, () = trace_to_subjaxpr_dynamic(fun, self.main, in_avals)
    closed_fun_jaxpr = core.ClosedJaxpr(convert_constvars_jaxpr(fun_jaxpr), ())
    main_ = ref(self.main)

    @_memoize
    def jvp_jaxpr_thunk(*in_zeros):
      for store in jvp.stores: store and store.reset()
      nz_tangent_avals, zero_avals = partition_list(in_zeros, in_avals)
      jvp_, out_zeros = _jvp_jaxpr_zeros(jvp, in_zeros, tuple(zero_avals))
      in_avals_ = (*in_avals, *nz_tangent_avals)
      jaxpr, _, out_consts, () = trace_to_subjaxpr_dynamic(jvp_, main_(), in_avals_)
      return jaxpr, out_consts, out_zeros()

    out_tracers = [DynamicJaxprTracer(self, a) for a in out_avals]
    invars = map(self.getvar, tracers)
    constvars = map(self.getvar, map(self.instantiate_const, consts))
    outvars = map(self.makevar, out_tracers)
    eqn = new_jaxpr_eqn([*constvars, *invars], outvars, prim,
                        dict(call_jaxpr=closed_fun_jaxpr,
                             jvp_jaxpr_thunk=jvp_jaxpr_thunk,
                             num_consts=len(consts),
                             symbolic_zeros=symbolic_zeros),
                        fun_jaxpr.effects,
                        source_info_util.current())
    self.frame.add_eqn(eqn)
    return out_tracers

  def post_process_custom_jvp_call(self, out_tracers, _):
    assert False  # unreachable

  def process_custom_vjp_call(self, prim, fun, fwd, bwd, tracers, out_trees,
                              symbolic_zeros):
    in_avals = [t.aval for t in tracers]
    with core.new_sublevel():
      fun_jaxpr, out_avals, consts, () = trace_to_subjaxpr_dynamic(fun, self.main, in_avals)
    closed_fun_jaxpr = core.ClosedJaxpr(convert_constvars_jaxpr(fun_jaxpr), ())

    main_ = ref(self.main)

    @_memoize
    def fwd_jaxpr_from_zeros(*zeros):
      for store in fwd.stores: store and store.reset()
      fwd_ = _interleave_fun(fwd, zeros)
      return trace_to_subjaxpr_dynamic(fwd_, main_(), in_avals)[::2]

    out_tracers = [DynamicJaxprTracer(self, a) for a in out_avals]
    invars = map(self.getvar, tracers)
    constvars = map(self.getvar, map(self.instantiate_const, consts))
    outvars = map(self.makevar, out_tracers)
    eqn = new_jaxpr_eqn([*constvars, *invars], outvars, prim.initial_style,
                        dict(fun_jaxpr=closed_fun_jaxpr,
                             fwd_jaxpr_thunk=fwd_jaxpr_from_zeros,
                             num_consts=len(consts),
                             bwd=bwd, out_trees=out_trees,
                             symbolic_zeros=symbolic_zeros),
                        fun_jaxpr.effects,
                        source_info_util.current())
    self.frame.add_eqn(eqn)
    return out_tracers

  def post_process_custom_vjp_call(self, out_tracers, _):
    assert False  # unreachable

  def process_custom_transpose(self, prim, call, tracers, *,
                               transpose, out_types,
                               lin_tree, res_tree, out_tree):
    tracers_res, tracers_lin = split_list(tracers, [res_tree.num_leaves])

    in_avals_p = [t.aval for t in tracers]
    in_avals_t = [*[t.aval for t in tracers_res], *out_types]

    with core.new_sublevel():
      call_jaxpr, out_avals, call_consts, () = trace_to_subjaxpr_dynamic(
          call, self.main, in_avals_p)
    closed_call_jaxpr = core.ClosedJaxpr(
        convert_constvars_jaxpr(call_jaxpr), ())

    transpose_flat, in_tree2 = flatten_fun_nokwargs(
        lu.wrap_init(transpose), treedef_tuple((res_tree, out_tree)))

    main_ = ref(self.main)
    # the following thunk evaluates to a pair: transpose_jaxpr, transpose_consts
    @_memoize
    def transpose_jaxpr_thunk():
      for store in transpose_flat.stores: store.reset()
      jaxpr, _, consts, () = trace_to_subjaxpr_dynamic(
          transpose_flat, main_(), in_avals_t)
      return jaxpr, consts

    out_tracers = [DynamicJaxprTracer(self, a) for a in out_avals]
    invars = map(self.getvar, tracers)
    constvars = map(self.getvar, map(self.instantiate_const, call_consts))
    outvars = map(self.makevar, out_tracers)
    eqn = new_jaxpr_eqn([*constvars, *invars], outvars, prim,
                        dict(call_jaxpr=closed_call_jaxpr,
                             transpose_jaxpr_thunk=transpose_jaxpr_thunk,
                             out_types=out_types, res_tree=res_tree,
                             lin_tree=lin_tree, out_tree=out_tree),
                        closed_call_jaxpr.effects,
                        source_info_util.current())
    self.frame.add_eqn(eqn)
    return out_tracers
