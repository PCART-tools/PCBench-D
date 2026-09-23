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
