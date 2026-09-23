def _initial_style_jaxpr_attrs(fun: Callable, in_tree, in_avals,
                               primitive_name: str | None = None):
  jaxpr, consts, out_tree, attrs_tracked = _initial_style_open_jaxpr(
      fun, in_tree, in_avals, primitive_name)
  closed_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr))
  return closed_jaxpr, consts, out_tree, attrs_tracked
