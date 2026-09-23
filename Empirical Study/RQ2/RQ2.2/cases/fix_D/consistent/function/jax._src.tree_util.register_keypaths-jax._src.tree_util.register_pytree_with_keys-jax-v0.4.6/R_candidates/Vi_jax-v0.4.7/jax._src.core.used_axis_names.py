def used_axis_names(primitive: Primitive, params: ParamDict) -> Set[AxisName]:
  subst = NameGatheringSubst()
  subst_axis_names(primitive, params, subst)
  return subst.axis_names
