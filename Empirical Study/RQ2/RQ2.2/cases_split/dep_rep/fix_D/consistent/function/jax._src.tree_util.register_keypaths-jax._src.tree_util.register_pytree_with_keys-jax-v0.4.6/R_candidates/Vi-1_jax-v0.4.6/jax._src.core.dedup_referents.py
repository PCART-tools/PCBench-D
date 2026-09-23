def dedup_referents(itr: Iterable[Any]) -> List[Any]:
  return list({HashableWrapper(get_referent(x)):x for x in itr}.values())
