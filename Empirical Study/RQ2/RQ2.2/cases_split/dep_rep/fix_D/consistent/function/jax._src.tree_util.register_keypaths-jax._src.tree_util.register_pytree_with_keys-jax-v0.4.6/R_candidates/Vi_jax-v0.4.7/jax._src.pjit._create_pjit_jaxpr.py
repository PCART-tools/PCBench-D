@lu.cache
def _create_pjit_jaxpr(fun, in_type, debug_info, out_paths):
  with dispatch.log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                                  "for pjit in {elapsed_time} sec",
                                  event=dispatch.JAXPR_TRACE_EVENT):
    pe_debug = debug_info and pe.debug_info_final(fun, debug_info.traced_for)
    if config.jax_dynamic_shapes:
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic2(
          lu.annotate(fun, in_type), debug_info=pe_debug)
    else:
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic(
          fun, in_type, debug_info=pe_debug)

  if not config.jax_dynamic_shapes:
    jaxpr = jaxpr_debug_info(jaxpr, debug_info, out_paths())

  if any(isinstance(c, core.Tracer) for c in consts):
    closed_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr))
    final_consts = consts
  else:
    closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
    final_consts = []
  return closed_jaxpr, final_consts, global_out_avals
