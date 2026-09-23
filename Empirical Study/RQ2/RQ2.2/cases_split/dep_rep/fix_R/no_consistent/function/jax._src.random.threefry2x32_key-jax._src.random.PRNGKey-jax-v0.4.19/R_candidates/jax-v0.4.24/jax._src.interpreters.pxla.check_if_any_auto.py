def check_if_any_auto(
    shardings: Iterable[(sharding_impls.XLACompatibleSharding |
                              AUTO | UnspecifiedValue)]) -> bool:
  for s in shardings:
    if is_auto(s):
      return True
  return False
