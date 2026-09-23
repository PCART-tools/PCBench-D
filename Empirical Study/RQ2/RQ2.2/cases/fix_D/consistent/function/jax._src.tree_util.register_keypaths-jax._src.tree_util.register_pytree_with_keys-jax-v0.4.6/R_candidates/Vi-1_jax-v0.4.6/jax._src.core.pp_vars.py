def pp_vars(vs: Sequence[Any], context: JaxprPpContext,
            *, separator="", print_shapes: bool = False) -> pp.Doc:
  if print_shapes:
    return pp.nest(2, pp.group(
      pp.join(pp.text(separator) + pp.group(pp.brk()), [
        pp.text(pp_var(v, context)) +
        pp.type_annotation(pp.text(":" + pp_aval(v.aval, context)))
        for v in vs
      ])
    ))
  else:
    return pp.nest(2, pp.group(
      pp.join(pp.text(separator) + pp.group(pp.brk()),
              [pp.text(pp_var(v, context)) for v in vs])
    ))
