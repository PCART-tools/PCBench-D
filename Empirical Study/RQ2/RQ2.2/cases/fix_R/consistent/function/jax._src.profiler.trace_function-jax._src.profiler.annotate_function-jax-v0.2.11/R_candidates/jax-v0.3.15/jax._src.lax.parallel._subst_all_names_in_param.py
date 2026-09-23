def _subst_all_names_in_param(
    pname: str, params: core.ParamDict, subst: core.AxisSubst, traverse: bool) -> core.ParamDict:
  axis_name = params[pname]
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  result = dict(params)
  result[pname] = sum(((name,) if isinstance(name, int) else subst(name)
                       for name in axis_name),
                      ())
  return result
