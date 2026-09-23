@partial(lu.cache, explain=explain_tracing_cache_miss)
def _create_pjit_jaxpr(fun, in_type, debug_info, out_paths, ignored_inline):
  del ignored_inline  # just for explain_cache_miss
  with dispatch.log_elapsed_time(
      "Finished tracing + transforming {fun_name} for pjit in {elapsed_time} sec",
      fun_name=fun.__name__, event=dispatch.JAXPR_TRACE_EVENT):
    pe_debug = debug_info and pe.debug_info_final(fun, debug_info.traced_for)
    if config.dynamic_shapes.value:
      jaxpr, global_out_avals, consts = pe.trace_to_jaxpr_dynamic2(
          lu.annotate(fun, in_type), debug_info=pe_debug)
      attrs_tracked = []
    else:
      jaxpr, global_out_avals, consts, attrs_tracked = pe.trace_to_jaxpr_dynamic(
          fun, in_type, debug_info=pe_debug)

  # TODO(dougalm,mattjj): enable debug info with attrs_tracked
  if not config.dynamic_shapes.value and not attrs_tracked:
    jaxpr = jaxpr_debug_info(jaxpr, debug_info, out_paths())

  if config.enable_key_reuse_checks.value:
    # Import here to avoid circular imports
    from jax.experimental.key_reuse._core import check_key_reuse_jaxpr
    check_key_reuse_jaxpr(jaxpr)

  if any(isinstance(c, core.Tracer) for c in consts):
    closed_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr))
    final_consts = consts
  else:
    closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
    final_consts = []
  return closed_jaxpr, final_consts, global_out_avals, attrs_tracked
