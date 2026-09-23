def used_axis_names(primitive: Primitive, params: ParamDict) -> set[AxisName]:
  subst = NameGatheringSubst()
  subst_axis_names(primitive, params, subst)
  return subst.axis_names
