def subst_axis_names_jaxpr(jaxpr: Union[Jaxpr, ClosedJaxpr], subst: AxisSubst):
  if isinstance(subst, NameGatheringSubst):  # This is a common case, so we optimize it!
    subst.axis_names |= used_axis_names_jaxpr(jaxpr)
    return jaxpr
  return do_subst_axis_names_jaxpr(jaxpr, subst)
