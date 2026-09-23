@lu.cache
def _create_pjit_jaxpr(fun, global_in_avals, api_name):
  prev_positional_val = pxla.positional_semantics.val
  try:
    pxla.positional_semantics.val = pxla._PositionalSemantics.GLOBAL
    with dispatch.log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                                   "for pjit in {elapsed_time} sec",
                                    event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic(
          fun, global_in_avals, debug_info=pe.debug_info_final(fun, api_name))
  finally:
    pxla.positional_semantics.val = prev_positional_val

  if any(isinstance(c, core.Tracer) for c in consts):
    jaxpr = pe.convert_constvars_jaxpr(jaxpr)
    jaxpr = pe.close_jaxpr(jaxpr)
    final_consts = consts
  else:
    jaxpr = core.ClosedJaxpr(jaxpr, consts)
    final_consts = []
  return jaxpr, final_consts, global_out_avals
