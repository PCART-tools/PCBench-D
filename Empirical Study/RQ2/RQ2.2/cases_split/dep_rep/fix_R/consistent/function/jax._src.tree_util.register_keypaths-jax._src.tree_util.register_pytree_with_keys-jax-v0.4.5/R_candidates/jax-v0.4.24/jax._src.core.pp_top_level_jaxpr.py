def pp_top_level_jaxpr(
    name: str,
    jaxpr: Jaxpr,
    context: JaxprPpContext,
    settings: JaxprPpSettings,
) -> pp.Doc:
  return pp.concat([
      pp.text("let " + name + " = "),
      pp_jaxpr(jaxpr, context, settings),
      pp.text(" in"),
      pp.brk(),
  ])
