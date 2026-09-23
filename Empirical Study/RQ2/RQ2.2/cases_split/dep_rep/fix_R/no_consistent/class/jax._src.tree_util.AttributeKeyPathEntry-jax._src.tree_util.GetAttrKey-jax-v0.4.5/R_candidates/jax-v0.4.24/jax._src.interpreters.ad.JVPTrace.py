class JVPTrace(Trace):

  def pure(self, val):
    tangent_zero = Zero(get_aval(val).at_least_vspace())
    return JVPTracer(self, val, tangent_zero)

  def lift(self, val):
    tangent_zero = Zero(get_aval(val).at_least_vspace())
    return JVPTracer(self, val, tangent_zero)

  def sublift(self, val):
    return JVPTracer(self, val.primal, val.tangent)

  def process_primitive(self, primitive, tracers, params):
    primals_in, tangents_in = unzip2((t.primal, t.tangent) for t in tracers)
    jvp = primitive_jvps.get(primitive)
    if not jvp:
      msg = f"Differentiation rule for '{primitive}' not implemented"
      raise NotImplementedError(msg)
    primal_out, tangent_out = jvp(primals_in, tangents_in, **params)
    if primitive.multiple_results:
      return [JVPTracer(self, x, t) for x, t in zip(primal_out, tangent_out)]
    else:
      return JVPTracer(self, primal_out, tangent_out)

  def process_call(self, call_primitive, f, tracers, params):
    assert call_primitive.multiple_results
    primals, tangents = unzip2((t.primal, t.tangent) for t in tracers)
    which_nz = [     type(t) is not Zero           for t in tangents]
    tangents = [t if type(t) is not Zero else None for t in tangents]
    args, in_tree = tree_flatten((primals, tangents))
    f_jvp = jvp_subtrace(f, self.main)
    f_jvp, which_nz_out = nonzero_tangent_outputs(f_jvp)
    if isinstance(call_primitive, core.MapPrimitive):
      in_axes = params['in_axes']
      tangent_in_axes = [ax for ax, nz in zip(in_axes, which_nz) if nz]
      out_axes_thunk = params['out_axes_thunk']
      # NOTE: This assumes that the output tangents being zero is a
      # deterministic function of which input tangents were zero.
      @as_hashable_function(closure=out_axes_thunk)
      def new_out_axes_thunk():
        out_ax = out_axes_thunk()
        return (*out_ax, *(ax for ax, nz in zip(out_ax, which_nz_out()) if nz))
      params = dict(params, in_axes=(*in_axes, *tangent_in_axes),
                    out_axes_thunk=new_out_axes_thunk)
    f_jvp, out_tree = traceable(f_jvp, in_tree)
    update_params = call_param_updaters.get(call_primitive)
    new_params = update_params(params, which_nz) if update_params else params
    result = call_primitive.bind(_update_annotation(f_jvp, f.in_type, which_nz),
                                 *args, **new_params)
    primal_out, tangent_out = tree_unflatten(out_tree(), result)
    tangent_out = [Zero(get_aval(p).at_least_vspace()) if t is None else t
                   for p, t in zip(primal_out, tangent_out)]
    return [JVPTracer(self, p, t) for p, t in zip(primal_out, tangent_out)]

  def post_process_call(self, call_primitive, out_tracers, params):
    primals, tangents = unzip2((t.primal, t.tangent) for t in out_tracers)
    out, treedef = tree_flatten((primals, tangents))
    tangents_nz = [type(t) is not Zero for t in tangents]
    del primals, tangents
    main = self.main
    def todo(x):
      primals, tangents = tree_unflatten(treedef, x)
      trace = JVPTrace(main, core.cur_sublevel())
      return map(partial(JVPTracer, trace), primals, tangents)
    if call_primitive.map_primitive:
      def out_axes_transform(out_axes):
        return (*out_axes, *(ax for ax, nz in zip(out_axes, tangents_nz) if nz))
      todo = (todo, out_axes_transform)
    return out, todo

  # The only difference between process_map and process_call is that
  # the `in_axes` and `out_axes_thunk` params must be updated;
  # that's handled in process_call.
  process_map = process_call
  post_process_map = post_process_call

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

  def post_process_custom_jvp_call(self, out_tracers, _):
    raise CustomJVPException()

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

  def post_process_custom_vjp_call(self, out_tracers, _):
    raise CustomVJPException()

  def process_custom_transpose(self, prim, call, tracers, **params):
    ps_in, ts_in = unzip2((t.primal, t.tangent) for t in tracers)
    res_ps_in, lin_ps_in = split_list(ps_in, [params['res_tree'].num_leaves])
    res_ts_in, lin_ts_in = split_list(ts_in, [params['res_tree'].num_leaves])

    # TODO(frostig): Handle differentiation with respect to residual
    # operands. Calling `call` twice on all operands invalid, since it
    # isn't linear in the residuals. However, we know that if we
    # write:
    #
    #   jvp_call_res = lambda x: partial(jvp, lambda r: call(r, x))
    #
    # then:
    #
    #   jvp(call, (r, x), (dr, dx)) == jvp_call_res(x)(r, dr) + call(r, dx)
    #
    # In words: a possible strategy is to take the jvp of `call` with
    # respect to residuals, and with linear arguments fixed, then add
    # that to a custom-transpose call to `call` (i.e. what we already
    # do below in the all-linear argument case).

    if any(type(t) is not Zero for t in res_ts_in):
      raise NotImplementedError(
        'JVP of custom transpose with respect to non-symbolic-zero residuals')

    ps_out = prim.bind(call, *ps_in, **params)

    lin_ts_in = map(instantiate_zeros, lin_ts_in)
    ts_out = prim.bind(call, *res_ps_in, *lin_ts_in, **params)

    return map(partial(JVPTracer, self), ps_out, ts_out)

  def join(self, xt, yt):
    xz, yz = type(xt) is Zero, type(yt) is Zero
    if xz == yz:
      return xt, yt
    elif yz and not xz:
      return xt, zeros_like_jaxval(xt)
    elif xz and not yz:
      return zeros_like_jaxval(yt), yt
    else:
      raise TypeError((xt, yt))
