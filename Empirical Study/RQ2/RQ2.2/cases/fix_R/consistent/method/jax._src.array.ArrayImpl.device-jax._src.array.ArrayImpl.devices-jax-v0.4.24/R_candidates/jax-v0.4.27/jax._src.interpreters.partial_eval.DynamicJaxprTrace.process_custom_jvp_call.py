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
