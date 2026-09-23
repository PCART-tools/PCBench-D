@cache_wrap
def _trace_to_jaxpr_and_dce(fun_or_jaxpr, global_in_avals, api_name, fun_name,
                            keep_unused, donated_invars, auto_spmd_lowering):
  name_stack = source_info_util.new_name_stack(wrap_name(fun_name, api_name))

  if isinstance(fun_or_jaxpr, lu.WrappedFun):
    with dispatch.log_elapsed_time(
        "Finished tracing + transforming {fun_name} in {elapsed_time} sec",
        fun_name=str(name_stack), event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_final(
          fun_or_jaxpr, global_in_avals)
  else:
    assert isinstance(fun_or_jaxpr, core.ClosedJaxpr)
    jaxpr = fun_or_jaxpr.jaxpr
    global_out_avals = fun_or_jaxpr.out_avals
    consts = fun_or_jaxpr.consts

  if (keep_unused or auto_spmd_lowering or
      any(hasattr(a, "shape") and not core.is_constant_shape(a.shape)
          for a in global_in_avals)):
    kept_var_idx = set(range(len(global_in_avals)))
  else:
    jaxpr, kept_const_idx, kept_var_idx = prune_unused_inputs(jaxpr)
    consts = [c for i, c in enumerate(consts) if i in kept_const_idx]
    global_in_avals = tuple(a for i, a in enumerate(global_in_avals) if i in kept_var_idx)
    donated_invars = tuple(x for i, x in enumerate(donated_invars) if i in kept_var_idx)
    del kept_const_idx

  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  return (closed_jaxpr, global_in_avals, tuple(global_out_avals), donated_invars,
          kept_var_idx, name_stack)
