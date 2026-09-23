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
      jaxpr, _, consts, atr = trace_to_subjaxpr_dynamic(fwd_, main_(), in_avals)
      if atr: raise NotImplementedError
      return jaxpr, consts

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
