def check_if_any_auto(
    shardings: Iterable[Union[sharding_internal.XLACompatibleSharding,
                              AUTOAxisResource, UnspecifiedValue]]) -> bool:
  for s in shardings:
    if is_auto(s):
      return True
  return False
