def pjit_staging_rule(trace, *args, **params):
  if (params["inline"] and
      all(_is_unspecified(i) for i in params["in_shardings"]) and
      all(_is_unspecified(o) for o in params["out_shardings"])):
    jaxpr = params['jaxpr']
    return core.eval_jaxpr(jaxpr.jaxpr, jaxpr.consts, *args)
  else:
    return trace.default_process_primitive(pjit_p, args, params)
