def check_all_or_none_unspecified(axis_resources, name):
  if not axis_resources:
    return False
  unspecified_count = 0
  unspecified = is_unspecified(axis_resources[0])
  for resource in axis_resources:
    current_is_unspecified = is_unspecified(resource)
    if current_is_unspecified:
      unspecified_count += 1
      assert unspecified_count == 1
    if current_is_unspecified != unspecified:
      raise ValueError(f'`pjit.UNSPECIFIED` exists in {name}. '
                       f'Make sure that every entry in {name} is '
                       '`pjit.UNSPECIFIED`.')
  return unspecified
