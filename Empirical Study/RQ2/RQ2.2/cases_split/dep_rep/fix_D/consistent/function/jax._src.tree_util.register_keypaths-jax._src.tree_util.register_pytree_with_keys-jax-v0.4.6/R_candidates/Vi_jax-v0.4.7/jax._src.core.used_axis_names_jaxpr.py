@weakref_lru_cache
def used_axis_names_jaxpr(jaxpr: Union[Jaxpr, ClosedJaxpr]):
  subst = NameGatheringSubst()
  do_subst_axis_names_jaxpr(jaxpr, subst)
  return frozenset(subst.axis_names)
